#!/usr/bin/env bash
# Extra 14B APPS runs (Nov 2026), parallel streams against ONE vLLM endpoint (L40S).
# Original MCTS ran on H200; L40S is ~3x slower per stream, so the per-problem wall-clock
# cap is raised 900 -> 3600 s (never binding in the original run: max 861 s) and the
# request timeout 180 -> 600 s. Token / call / code-generation budgets are unchanged.
# Usage: ENDPOINT=https://.../v1 bash scripts/launch_extra_14b.sh [apps|humaneval]
set -euo pipefail
: "${ENDPOINT:?set ENDPOINT to the OpenAI-compatible base URL ending in /v1}"
WHAT="${1:-apps}"
A=configs/extra_14b/apps_14b_base.yaml
H=configs/extra_14b/humaneval_14b_base.yaml
COMMON=(--set "model.base_url=$ENDPOINT" --set budget.max_wall_seconds=3600 --set model.request_timeout_seconds=600)
mkdir -p logs/extra_14b
launch() {
  local name="$1"; shift
  echo "[$(date +%T)] start $name"
  nohup python3 scripts/run_benchmark_batch.py "$@" --output-dir "runs/$name" "${COMMON[@]}" \
    > "logs/extra_14b/$name.log" 2>&1 &
  echo "$!" > "logs/extra_14b/$name.pid"
}
if [ "$WHAT" = apps ]; then
  for q in 1 2 3 4; do
    launch "benchmark_apps_14b_norethink_q$q" --config $A --solver mcts \
      --problem-ids "@data/batches/extra_apps_q$q.json" --set search.max_rethinks_per_node=0
    launch "benchmark_apps_14b_repair_q$q" --config $A --solver iterative_repair \
      --problem-ids "@data/batches/extra_apps_q$q.json"
  done
  launch benchmark_apps_14b_bon3_rest140 --config $A --solver best_of_n --samples-n 3 \
    --problem-ids @data/batches/bon3_rest_140.json
elif [ "$WHAT" = humaneval ]; then
  launch humaneval_direct_14b_v2 --config $H --solver direct --dataset humaneval
  launch humaneval_bon3_14b_v2 --config $H --solver best_of_n --samples-n 3 --dataset humaneval
fi
