#!/usr/bin/env bash
# =============================================================================
# launch_10gpu_benchmark.sh
# Run 10 parallel APPS benchmark batches across 10 GPU endpoints.
#
# Usage:
#   # Launch all 10 batches in background:
#   bash scripts/launch_10gpu_benchmark.sh
#
#   # Or launch specific batches:
#   bash scripts/launch_10gpu_benchmark.sh 1 2 3
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

if [ "$#" -gt 0 ]; then
    BATCHES=("$@")
else
    BATCHES=(1 2 3 4 5 6 7 8 9 10)
fi

mkdir -p runs logs

echo "================================================================="
echo "  RethinkMCTS 14B Dual-Policy Benchmark (10-GPU Parallel Runner)"
echo "  Batches to run: ${BATCHES[*]}"
echo "================================================================="

PIDS=()
BATCH_DIRS=()

for b in "${BATCHES[@]}"; do
    BID=$(printf "batch_%02d" "$b")
    CFG="configs/batches/${BID}.yaml"
    PIDS_FILE="data/batches/${BID}.json"
    OUT_DIR="runs/benchmark_14b_${BID}"
    LOG_FILE="logs/${BID}.log"

    if [ ! -f "${CFG}" ]; then
        echo "❌ Error: Config file ${CFG} not found. Run scripts/gen_10gpu_configs.py first."
        exit 1
    fi

    if [ ! -f "${PIDS_FILE}" ]; then
        echo "❌ Error: Batch file ${PIDS_FILE} not found. Run scripts/split_cohort_10way.py first."
        exit 1
    fi

    BATCH_DIRS+=("${OUT_DIR}")

    echo "🚀 Starting ${BID} in background (logging to ${LOG_FILE})..."
    python3 scripts/run_benchmark_batch.py \
        --config "${CFG}" \
        --dataset apps \
        --solver mcts \
        --samples-n 3 \
        --output-dir "${OUT_DIR}" \
        --problem-ids "@${PIDS_FILE}" \
        > "${LOG_FILE}" 2>&1 &

    PID=$!
    PIDS+=("${PID}")
    echo "   [${BID}] Process PID: ${PID}"
done

echo "================================================================="
echo "All ${#PIDS[@]} batches launched in background."
echo "Monitoring progress... (Press Ctrl+C to stop monitoring; jobs will continue)"
echo "================================================================="

FAILED=0
for i in "${!PIDS[@]}"; do
    pid="${PIDS[$i]}"
    bid=$(printf "batch_%02d" "${BATCHES[$i]}")
    if wait "$pid"; then
        echo "✅ [${bid}] Finished successfully."
    else
        echo "❌ [${bid}] Exited with error! Check logs/${bid}.log"
        FAILED=$((FAILED + 1))
    fi
done

echo "================================================================="
if [ "$FAILED" -eq 0 ]; then
    echo "🎉 All batches completed successfully!"
    echo "Merging results into unified run directory..."
    python3 scripts/merge_apps_batches.py \
        --batch-dirs "${BATCH_DIRS[@]}" \
        --output-dir "runs/benchmark_apps_14b_dual_unified"
    echo "✅ Benchmark run complete. Summary saved at runs/benchmark_apps_14b_dual_unified/summary.md"
else
    echo "⚠️  ${FAILED} batch(es) failed. Inspect the log files in logs/."
fi
