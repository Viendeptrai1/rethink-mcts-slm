#!/usr/bin/env python3
"""
prepare_retry_batches.py
Extracts the 80 uncompleted problem IDs from batch_01..04
and configures 4 retry batches pointing to vienphanquoc-123's 4 active GPUs.
"""
import json
import yaml
from pathlib import Path

BASE_CONFIG = Path("configs/benchmark_apps_14b_dual.yaml")
ENDPOINTS = {
    1: "https://vienphanquoc-123--rethink-vllm-a-serve.modal.run/v1",
    2: "https://vienphanquoc-123--rethink-vllm-b-serve.modal.run/v1",
    3: "https://vienphanquoc-123--rethink-vllm-c-serve.modal.run/v1",
    4: "https://vienphanquoc-123--rethink-vllm-d-serve.modal.run/v1",
}


def main():
    base_cfg = yaml.safe_load(BASE_CONFIG.read_text())

    total_missing = 0
    for i in range(1, 5):
        bid = f"batch_{i:02d}"
        batch_json = Path(f"data/batches/{bid}.json")
        all_pids = json.loads(batch_json.read_text())["problem_ids"]

        bdir = Path(f"runs/benchmark_14b_{bid}/problems")
        completed_pids = set()
        if bdir.exists():
            completed_pids = {p.name for p in bdir.iterdir() if (p / "completed.json").exists()}

        missing_pids = [p for p in all_pids if p not in completed_pids]
        total_missing += len(missing_pids)

        rid = f"retry_{i:02d}"
        endpoint = ENDPOINTS[i]

        # 1. Write batch json
        payload = {
            "batch_id": rid,
            "original_batch": bid,
            "endpoint": endpoint,
            "problem_ids": missing_pids
        }
        out_batch = Path(f"data/batches/{rid}.json")
        out_batch.write_text(json.dumps(payload, indent=2))

        # 2. Write YAML config
        cfg = json.loads(json.dumps(base_cfg))
        cfg["model"]["base_url"] = endpoint
        out_cfg = Path(f"configs/batches/{rid}.yaml")
        out_cfg.write_text(yaml.dump(cfg, default_flow_style=False, allow_unicode=True))

        print(f"[{rid}] {len(missing_pids)} missing problems → {endpoint}")

    print(f"\n✅ Total missing problems configured: {total_missing}/80")


if __name__ == "__main__":
    main()
