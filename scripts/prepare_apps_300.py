"""
Fetch and prepare exactly 300 APPS problems (100 Introductory, 100 Interview, 100 Competition)
matching Section 5 (Datasets) of the RethinkMCTS paper.
"""

import os
import json
import requests
from rethink_mcts.application.prepare import prepare_dataset

APPS_URL = "https://huggingface.co/datasets/codeparrot/apps/resolve/main/test.jsonl"
RAW_OUT = "data/apps/apps_300.jsonl"
PREPARED_DIR = "prepared/apps"
TARGET_PER_DIFF = 100

def fetch_and_prepare():
    os.makedirs("data/apps", exist_ok=True)
    counts = {"introductory": 0, "interview": 0, "competition": 0}
    collected = []
    scanned = 0

    print(f"Downloading APPS test split from Hugging Face ({APPS_URL})...")
    print(f"Target: {TARGET_PER_DIFF} Introductory + {TARGET_PER_DIFF} Interview + {TARGET_PER_DIFF} Competition = 300 problems.")

    with requests.get(APPS_URL, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(chunk_size=1024 * 1024):
            if not line:
                continue
            scanned += 1
            try:
                item = json.loads(line.decode("utf-8"))
            except Exception:
                continue

            diff = str(item.get("difficulty", "")).lower()
            if diff in counts and counts[diff] < TARGET_PER_DIFF:
                counts[diff] += 1
                collected.append(item)
                if len(collected) % 25 == 0 or len(collected) == 300:
                    print(f"Progress: {len(collected)}/300 collected (Intro: {counts['introductory']}, Inter: {counts['interview']}, Comp: {counts['competition']}, Scanned: {scanned})")

            if all(c >= TARGET_PER_DIFF for c in counts.values()):
                break

    print(f"\nCompleted collection: {len(collected)} total problems from {scanned} scanned.")
    with open(RAW_OUT, "w", encoding="utf-8") as f:
        for item in collected:
            f.write(json.dumps(item) + "\n")
    print(f"Saved raw 300 APPS records to {RAW_OUT}.")

    print("\nPreparing separated public and hidden judge stores...")
    manifest = prepare_dataset(
        dataset_name="apps",
        raw_path=RAW_OUT,
        output_dir=PREPARED_DIR,
        limit=300
    )
    print(f"✓ Successfully prepared {manifest['total_problems']} APPS problems into {PREPARED_DIR}/")
    print(f"  Public problems: {manifest['public_problems_path']}")
    print(f"  Judge suites: {manifest['judge_suites_dir']}")

if __name__ == "__main__":
    fetch_and_prepare()
