#!/usr/bin/env python3
"""
gen_10gpu_configs.py
Generate 10 per-batch YAML configs for the 14B benchmark run,
each pointing to a unique Modal vLLM endpoint.
Reads batch files from data/batches/ and writes configs to configs/batches/.
"""
import json
import yaml
from pathlib import Path

BATCH_DIR = Path("data/batches")
CONFIG_OUT_DIR = Path("configs/batches")
BASE_CONFIG = Path("configs/benchmark_apps_14b_dual.yaml")


def main():
    base = yaml.safe_load(BASE_CONFIG.read_text())
    CONFIG_OUT_DIR.mkdir(parents=True, exist_ok=True)

    batch_files = sorted(BATCH_DIR.glob("batch_*.json"))
    if not batch_files:
        raise SystemExit(f"No batch files found in {BATCH_DIR}. Run split_cohort_10way.py first.")

    for bf in batch_files:
        meta = json.loads(bf.read_text())
        batch_id = meta["batch_id"]    # e.g. "batch_01"
        endpoint = meta["endpoint"]    # e.g. "https://..."

        cfg = json.loads(json.dumps(base))  # deep copy via JSON round-trip
        cfg["model"]["base_url"] = endpoint

        out_path = CONFIG_OUT_DIR / f"{batch_id}.yaml"
        out_path.write_text(yaml.dump(cfg, default_flow_style=False, allow_unicode=True))
        print(f"  {out_path} → {endpoint}")

    print(f"\n✅ {len(batch_files)} config files written to {CONFIG_OUT_DIR}/")


if __name__ == "__main__":
    main()
