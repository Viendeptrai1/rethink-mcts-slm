#!/usr/bin/env python3
"""
split_cohort_10way.py
Split the 300-problem APPS cohort into 10 balanced batch files (30 problems each).

Batch → Account assignment:
  01, 02, 03  →  phanquocvien-123   (rethink-vllm-a/b/c)
  04, 05, 06  →  kotorikotorii0     (rethink-vllm-a/b/c)
  07, 08      →  phanquocvien-1234  (rethink-vllm-a/b)
  09, 10      →  vienphanquoc-123   (rethink-vllm-a/b)

Output: data/batches/batch_XX.json  (each with 30 problem IDs)
        data/batches/README.md      (endpoint mapping table)
"""
import json
from pathlib import Path

COHORT_FILE = Path("data/cohorts/apps_benchmark_300.json")
OUT_DIR = Path("data/batches")
N_BATCHES = 10

# Endpoint map: batch index (1-based) → (modal_profile, app_name)
BATCH_ENDPOINTS = {
    1:  ("phanquocvien-123",  "rethink-vllm-a"),
    2:  ("phanquocvien-123",  "rethink-vllm-b"),
    3:  ("phanquocvien-123",  "rethink-vllm-c"),
    4:  ("phanquocvien-123",  "rethink-vllm-d"),
    5:  ("kotorikotorii0",    "rethink-vllm-a"),
    6:  ("kotorikotorii0",    "rethink-vllm-b"),
    7:  ("kotorikotorii0",    "rethink-vllm-c"),
    8:  ("vienphanquoc-123",  "rethink-vllm-a"),
    9:  ("vienphanquoc-123",  "rethink-vllm-b"),
    10: ("vienphanquoc-123",  "rethink-vllm-c"),
}


def main():
    raw = json.loads(COHORT_FILE.read_text())
    ids = [x.strip() for x in raw["problem_ids_csv"].split(",") if x.strip()]
    assert len(ids) == 300, f"Expected 300 IDs, got {len(ids)}"

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Split into N_BATCHES equal chunks
    chunk_size = len(ids) // N_BATCHES  # 30
    batches = []
    for i in range(N_BATCHES):
        start = i * chunk_size
        end = start + chunk_size if i < N_BATCHES - 1 else len(ids)
        batches.append(ids[start:end])

    readme_lines = [
        "# Batch → Endpoint Mapping\n",
        "| Batch | Problems | Profile | App Name | Endpoint |",
        "|-------|----------|---------|----------|----------|",
    ]

    for idx, chunk in enumerate(batches, start=1):
        profile, app = BATCH_ENDPOINTS[idx]
        endpoint = f"https://{profile}--{app}-serve.modal.run/v1"
        out_file = OUT_DIR / f"batch_{idx:02d}.json"
        payload = {
            "batch_id": f"batch_{idx:02d}",
            "endpoint": endpoint,
            "profile": profile,
            "app_name": app,
            "problem_ids": chunk,
        }
        out_file.write_text(json.dumps(payload, indent=2))
        print(f"  batch_{idx:02d}.json → {len(chunk)} problems → {endpoint}")
        readme_lines.append(
            f"| {idx:02d} | {chunk[0]} … {chunk[-1]} ({len(chunk)}) | {profile} | {app} | {endpoint} |"
        )

    (OUT_DIR / "README.md").write_text("\n".join(readme_lines) + "\n")
    print(f"\n✅ {N_BATCHES} batch files written to {OUT_DIR}/")


if __name__ == "__main__":
    main()
