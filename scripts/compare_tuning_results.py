#!/usr/bin/env python3
"""
Summarize and compare hyperparameter tuning experiment runs.
Reads manifests and summary/problem records to produce clean markdown comparison tables.
"""

import json
import sys
from pathlib import Path


def inspect_run(run_dir: Path) -> dict:
    manifest_path = run_dir / "manifest.json"
    summary_path = run_dir / "summary.json"

    if not manifest_path.exists():
        return None

    with open(manifest_path) as f:
        manifest = json.load(f)

    cfg = manifest.get("config", manifest.get("effective_config", {}))
    search_cfg = cfg.get("search", {})
    reward_cfg = cfg.get("reward", {})
    model_cfg = cfg.get("model", {})

    run_info = {
        "run_dir": run_dir.name,
        "c_param": search_cfg.get("c"),
        "c_base": search_cfg.get("c_base"),
        "selection": search_cfg.get("selection"),
        "test_weight": reward_cfg.get("test_weight"),
        "llm_weight": reward_cfg.get("llm_weight"),
        "model": model_cfg.get("model", "").split("/")[-1],
        "problems": [],
        "completed": 0,
        "passed": 0,
        "total_calls": 0,
        "total_tokens": 0,
        "total_solve_sec": 0.0,
        "mean_hidden_pass_rate": 0.0,
    }

    if summary_path.exists():
        with open(summary_path) as f:
            summary = json.load(f)
        run_info["completed"] = summary.get("completed_problems", 0)
        run_info["passed"] = summary.get("passed_problems", 0)
        run_info["total_calls"] = summary.get("total_model_calls", 0)
        run_info["total_tokens"] = summary.get("total_tokens", 0)
        run_info["total_solve_sec"] = summary.get("solve_wall_seconds", 0.0)
        run_info["mean_hidden_pass_rate"] = summary.get("mean_hidden_pass_rate_completed", 0.0)
        run_info["results"] = summary.get("results", [])
    else:
        # Scan problems directory manually if summary.json is not yet created
        pdir = run_dir / "problems"
        if pdir.exists():
            rates = []
            for prob_p in pdir.iterdir():
                comp_file = prob_p / "completed.json"
                if comp_file.exists():
                    with open(comp_file) as f:
                        cdata = json.load(f)
                    run_info["completed"] += 1
                    if cdata.get("all_hidden_passed"):
                        run_info["passed"] += 1
                    usage = cdata.get("usage", {})
                    run_info["total_calls"] += usage.get("total_model_calls", 0)
                    t_roles = usage.get("tokens_by_role", {})
                    for r, tok in t_roles.items():
                        run_info["total_tokens"] += tok.get("input", 0) + tok.get("output", 0)
                    run_info["total_solve_sec"] += cdata.get("solve_wall_seconds", 0.0)
                    rate = cdata.get("hidden_pass_rate", 0.0)
                    rates.append(rate)
            if rates:
                run_info["mean_hidden_pass_rate"] = sum(rates) / len(rates)

    return run_info


def main():
    runs_dir = Path("runs")
    if not runs_dir.exists():
        print("No runs/ directory found.")
        return

    tuning_dirs = sorted([d for d in runs_dir.iterdir() if d.is_dir() and "tuning" in d.name])
    if not tuning_dirs:
        print("No tuning run directories found matching 'runs/*tuning*'.")
        return

    reports = []
    for d in tuning_dirs:
        info = inspect_run(d)
        if info:
            reports.append(info)

    print("\n### BẢNG SO SÁNH THỰC NGHIỆM TUNING SIÊU THAM SỐ (HYPERPARAMETER COMPARISON)")
    print("| Thư mục Run | C-Param | Reward (a/b) | Completed | Pass@1 Full | Mean Hidden Pass% | Avg Calls/Prob | Avg Time/Prob (s) |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    for r in reports:
        n_comp = r["completed"]
        avg_calls = f"{r['total_calls'] / n_comp:.1f}" if n_comp > 0 else "N/A"
        avg_time = f"{r['total_solve_sec'] / n_comp:.1f}s" if n_comp > 0 else "N/A"
        mean_rate = f"{r['mean_hidden_pass_rate'] * 100:.2f}%" if n_comp > 0 else "In progress..."
        pass_at_1 = f"{r['passed']}/{n_comp}" if n_comp > 0 else "0/0"
        reward_str = f"{r['test_weight']}/{r['llm_weight']}"
        print(f"| `{r['run_dir']}` | **c={r['c_param']}** | {reward_str} | {n_comp} | {pass_at_1} | **{mean_rate}** | {avg_calls} | {avg_time} |")
    print("\n")


if __name__ == "__main__":
    main()
