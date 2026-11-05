#!/usr/bin/env python3
"""
Cross-Critic Benchmark: Self-Critic (Qwen2.5-Coder-14B) vs Cross-Critic (Mistral Codestral)
Evaluates candidates that achieved 100% public test pass rate on APPS-300.
"""

import os
import sys
import json
import glob
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import numpy as np
from scipy import stats

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
OUTPUT_DIR = "runs/cross_critic_analysis_14b"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "cross_critic_results.json")
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "summary.json")

PROMPT_TEMPLATE = """You are a strict code correctness evaluator.
Problem statement:
{statement}

Reasoning path:
{reasoning_path}

Candidate code:
```python
{code}
```

The candidate already passes all public tests. Estimate whether it passes unseen edge cases. Return only JSON with one numeric key `evaluation` in [-1, 1]."""


def parse_critic_score(raw_text: str) -> float:
    try:
        data = json.loads(raw_text)
        if "evaluation" in data:
            val = float(data["evaluation"])
            return max(-1.0, min(1.0, val))
    except Exception:
        pass
    
    m = re.search(r'"evaluation"\s*:\s*([+-]?\d+(?:\.\d+)?)', raw_text)
    if m:
        try:
            val = float(m.group(1))
            return max(-1.0, min(1.0, val))
        except Exception:
            pass
            
    m2 = re.search(r'([+-]?\d+(?:\.\d+)?)', raw_text)
    if m2:
        try:
            val = float(m2.group(1))
            return max(-1.0, min(1.0, val))
        except Exception:
            pass
            
    return 0.0


def evaluate_with_codestral(item: dict, max_retries: int = 3) -> dict:
    thoughts = item.get("thoughts") or []
    reasoning_str = "\n".join(f"{i+1}. {t}" for i, t in enumerate(thoughts)) if thoughts else "(none)"

    prompt = PROMPT_TEMPLATE.format(
        statement=item["statement"],
        reasoning_path=reasoning_str,
        code=item["code"]
    )

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "codestral-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "response_format": {"type": "json_object"}
    }

    raw_response = None
    score = 0.0
    latency = 0.0

    for attempt in range(max_retries):
        try:
            t0 = time.time()
            resp = requests.post(MISTRAL_URL, headers=headers, json=payload, timeout=20)
            latency = time.time() - t0
            if resp.status_code == 200:
                raw_response = resp.json()["choices"][0]["message"]["content"]
                score = parse_critic_score(raw_response)
                break
            elif resp.status_code == 429:
                time.sleep(2.0 * (attempt + 1))
            else:
                time.sleep(1.0)
        except Exception as e:
            if attempt == max_retries - 1:
                raw_response = str(e)
            time.sleep(1.5)

    res = dict(item)
    res["cross_eval_raw"] = score
    res["cross_eval_latency"] = latency
    res["cross_eval_raw_response"] = raw_response
    return res


def compute_statistics(results: list) -> dict:
    self_scores = np.array([r["self_eval_raw"] for r in results])
    cross_scores = np.array([r["cross_eval_raw"] for r in results])
    hidden_rates = np.array([r["hidden_pass_rate"] for r in results])
    hidden_passed = np.array([1 if r["all_hidden_passed"] else 0 for r in results])

    self_pearson, self_p_p = stats.pearsonr(self_scores, hidden_rates)
    cross_pearson, cross_p_p = stats.pearsonr(cross_scores, hidden_rates)

    self_spearman, self_sp_p = stats.spearmanr(self_scores, hidden_rates)
    cross_spearman, cross_sp_p = stats.spearmanr(cross_scores, hidden_rates)

    self_pb, self_pb_p = stats.pointbiserialr(hidden_passed, self_scores)
    cross_pb, cross_pb_p = stats.pointbiserialr(hidden_passed, cross_scores)

    overfit_items = [r for r in results if not r["all_hidden_passed"]]
    passed_items = [r for r in results if r["all_hidden_passed"]]

    self_overfit_approved = sum(1 for r in overfit_items if r["self_eval_raw"] > 0)
    cross_overfit_approved = sum(1 for r in overfit_items if r["cross_eval_raw"] > 0)

    self_passed_approved = sum(1 for r in passed_items if r["self_eval_raw"] > 0)
    cross_passed_approved = sum(1 for r in passed_items if r["cross_eval_raw"] > 0)

    return {
        "total_evaluations": len(results),
        "total_passed_hidden": len(passed_items),
        "total_failed_hidden_overfit": len(overfit_items),
        "correlations": {
            "self_critic_qwen14b": {
                "pearson_r": float(self_pearson),
                "pearson_p": float(self_p_p),
                "spearman_rho": float(self_spearman),
                "spearman_p": float(self_sp_p),
                "point_biserial_r": float(self_pb),
                "point_biserial_p": float(self_pb_p)
            },
            "cross_critic_codestral": {
                "pearson_r": float(cross_pearson),
                "pearson_p": float(cross_p_p),
                "spearman_rho": float(cross_spearman),
                "spearman_p": float(cross_sp_p),
                "point_biserial_r": float(cross_pb),
                "point_biserial_p": float(cross_pb_p)
            }
        },
        "score_distributions": {
            "self_critic_qwen14b": {str(k): int(v) for k, v in zip(*np.unique(self_scores, return_counts=True))},
            "cross_critic_codestral": {str(k): int(v) for k, v in zip(*np.unique(cross_scores, return_counts=True))}
        },
        "discrimination": {
            "overfit_cases_total": len(overfit_items),
            "self_critic_false_approval_count": self_overfit_approved,
            "self_critic_false_approval_rate": self_overfit_approved / len(overfit_items) if overfit_items else 0,
            "cross_critic_false_approval_count": cross_overfit_approved,
            "cross_critic_false_approval_rate": cross_overfit_approved / len(overfit_items) if overfit_items else 0,
            "passed_cases_total": len(passed_items),
            "self_critic_true_approval_count": self_passed_approved,
            "self_critic_true_approval_rate": self_passed_approved / len(passed_items) if passed_items else 0,
            "cross_critic_true_approval_count": cross_passed_approved,
            "cross_critic_true_approval_rate": cross_passed_approved / len(passed_items) if passed_items else 0
        }
    }


def main():
    with open(OUTPUT_FILE) as f:
        data = json.load(f)

    stats_summary = compute_statistics(data)
    with open(SUMMARY_FILE, "w") as f:
        json.dump(stats_summary, f, indent=2)

    print("\n=== BENCHMARK SUMMARY ===")
    print(json.dumps(stats_summary, indent=2))


if __name__ == "__main__":
    main()
