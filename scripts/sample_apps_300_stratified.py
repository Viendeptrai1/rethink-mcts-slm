"""
Stratified Random Sampling for APPS Benchmark (300 problems).
Methodology:
- Source: Hugging Face APPS test split (5,000 problems).
- Strata: 1,000 Introductory, 3,000 Interview, 1,000 Competition.
- Filtering: Must have >= 3 test cases for strict disjoint public/hidden evaluation.
- Sampling: Stratified Uniform Random Sampling without replacement.
- Seed: 2027 (user-specified fixed seed for academic reproducibility).
- Sample Size: 100 per stratum (Total 300 problems).
"""

import os
import json
import random
import requests
import shutil
from collections import defaultdict
from rethink_mcts.application.prepare import prepare_dataset

APPS_URL = "https://huggingface.co/datasets/codeparrot/apps/resolve/main/test.jsonl"
SEED = 2027
TARGET_PER_STRATUM = 100
RAW_OUTPUT = "data/apps/apps_300_seed2027.jsonl"
PREPARED_DIR = "prepared/apps"
COHORT_MAIN = "data/cohorts/apps_benchmark_300.json"


def is_valid_problem(item: dict) -> bool:
    """Validate that problem has at least 3 test cases for public/hidden split."""
    io_data = item.get("input_output", "")
    if isinstance(io_data, str) and io_data.strip():
        try:
            io_data = json.loads(io_data)
        except Exception:
            return False
    if not isinstance(io_data, dict):
        return False
    inputs = io_data.get("inputs", [])
    outputs = io_data.get("outputs", [])
    return len(inputs) == len(outputs) and len(inputs) >= 3


def sample_apps():
    print(f"=== APPS Stratified Random Sampling (Seed: {SEED}) ===")
    print(f"Connecting to Hugging Face: {APPS_URL}")

    pools = defaultdict(list)
    total_scanned = 0

    with requests.get(APPS_URL, stream=True, timeout=180) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(chunk_size=1024 * 1024):
            if not line:
                continue
            total_scanned += 1
            try:
                item = json.loads(line.decode("utf-8"))
            except Exception:
                continue

            diff = str(item.get("difficulty", "")).lower()
            if diff in ("introductory", "interview", "competition"):
                if is_valid_problem(item):
                    # Strip huge solutions field to conserve memory
                    clean_item = {
                        "id": item.get("id"),
                        "problem_id": item.get("id"),
                        "question": item.get("question", ""),
                        "difficulty": diff,
                        "input_output": item.get("input_output", ""),
                        "starter_code": item.get("starter_code", ""),
                        "url": item.get("url", ""),
                    }
                    pools[diff].append(clean_item)

            if total_scanned % 500 == 0:
                print(f"Scanned {total_scanned} records... Valid pools: "
                      f"Intro: {len(pools['introductory'])}, "
                      f"Interview: {len(pools['interview'])}, "
                      f"Competition: {len(pools['competition'])}")

    print(f"\nScan complete. Total records scanned: {total_scanned}")
    for diff, items in pools.items():
        print(f"  {diff.capitalize()} pool size: {len(items)} eligible problems")

    # Perform Stratified Random Sampling with fixed seed
    random.seed(SEED)
    sampled = {}
    for diff in ["introductory", "interview", "competition"]:
        if len(pools[diff]) < TARGET_PER_STRATUM:
            raise RuntimeError(f"Pool for {diff} only has {len(pools[diff])} items, need {TARGET_PER_STRATUM}")
        # Sample 100 without replacement, then sort by ID for consistent indexing
        selected = random.sample(pools[diff], TARGET_PER_STRATUM)
        selected.sort(key=lambda x: x["id"])
        sampled[diff] = selected
        print(f"Sampled {len(selected)} {diff} problems (ID range: {selected[0]['id']} -> {selected[-1]['id']})")

    # Combine into 300 raw problems
    all_300 = sampled["introductory"] + sampled["interview"] + sampled["competition"]
    os.makedirs(os.path.dirname(RAW_OUTPUT), exist_ok=True)
    with open(RAW_OUTPUT, "w", encoding="utf-8") as f:
        for item in all_300:
            f.write(json.dumps(item) + "\n")
    print(f"\nSaved 300 sampled problems to {RAW_OUTPUT}")

    # Backup current prepared/apps if not backed up
    backup_dir = "prepared/apps_backup_seq"
    if os.path.exists(PREPARED_DIR) and not os.path.exists(backup_dir):
        print(f"Backing up existing sequential prepared/apps to {backup_dir}...")
        shutil.copytree(PREPARED_DIR, backup_dir)

    # Re-prepare dataset
    print(f"\nPreparing separate public and hidden suites in {PREPARED_DIR}...")
    manifest = prepare_dataset(
        dataset_name="apps",
        raw_path=RAW_OUTPUT,
        output_dir=PREPARED_DIR,
        limit=300
    )
    print(f"Successfully prepared {manifest['total_problems']} APPS problems into {PREPARED_DIR}/")

    # Build cohort JSON file
    intro_ids = [f"apps_{p['id']}" for p in sampled["introductory"]]
    inter_ids = [f"apps_{p['id']}" for p in sampled["interview"]]
    comp_ids = [f"apps_{p['id']}" for p in sampled["competition"]]
    all_ids = intro_ids + inter_ids + comp_ids

    cohort_data = {
        "cohort_id": f"apps_benchmark_300_stratified_seed{SEED}",
        "description": f"Full 300 APPS benchmark cohort sampled via Stratified Random Sampling (Seed {SEED}) across entire APPS test set",
        "sampling_method": {
            "strategy": "Stratified Random Sampling without replacement",
            "seed": SEED,
            "population_source": "Hugging Face codeparrot/apps (test.jsonl, 5000 problems)",
            "selection_criteria": "len(inputs) >= 3 and len(inputs) == len(outputs)",
            "strata": {
                "introductory": f"{len(intro_ids)} from {len(pools['introductory'])}",
                "interview": f"{len(inter_ids)} from {len(pools['interview'])}",
                "competition": f"{len(comp_ids)} from {len(pools['competition'])}"
            }
        },
        "target_ratio": {
            "introductory": len(intro_ids),
            "interview": len(inter_ids),
            "competition": len(comp_ids)
        },
        "total_problems": len(all_ids),
        "problem_ids_csv": ",".join(all_ids),
        "groups": {
            "introductory": intro_ids,
            "interview": inter_ids,
            "competition": comp_ids
        }
    }

    os.makedirs(os.path.dirname(COHORT_MAIN), exist_ok=True)
    with open(COHORT_MAIN, "w", encoding="utf-8") as f:
        json.dump(cohort_data, f, indent=2)
    print(f"Generated cohort file:\n  {COHORT_MAIN}")


if __name__ == "__main__":
    sample_apps()
