#!/usr/bin/env bash
# =============================================================================
# launch_retry_benchmark.sh
# Run the 80 remaining problems across 4 retry batches on vienphanquoc-123 GPUs.
# Upon completion, merges all 14 batch directories into the master 300 result.
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

RETRIES=(01 02 03 04)

mkdir -p runs logs

echo "================================================================="
echo "  RethinkMCTS 14B Dual Benchmark: Final 80 Problems on vienphanquoc-123"
echo "  Batches to run: ${RETRIES[*]}"
echo "================================================================="

PIDS=()
for b in "${RETRIES[@]}"; do
    BID="retry_${b}"
    CFG="configs/batches/${BID}.yaml"
    PIDS_FILE="data/batches/${BID}.json"
    OUT_DIR="runs/benchmark_14b_${BID}"
    LOG_FILE="logs/${BID}.log"

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
echo "All 4 retry batches running in background."
echo "Monitoring progress..."
echo "================================================================="

FAILED=0
for i in "${!PIDS[@]}"; do
    pid="${PIDS[$i]}"
    bid="retry_${RETRIES[$i]}"
    if wait "$pid"; then
        echo "✅ [${bid}] Finished successfully."
    else
        echo "❌ [${bid}] Exited with error! Check logs/${bid}.log"
        FAILED=$((FAILED + 1))
    fi
done

echo "================================================================="
if [ "$FAILED" -eq 0 ]; then
    echo "🎉 All retry batches completed successfully!"
    echo "Merging all 14 batch directories into master unified 300 dataset..."

    ALL_DIRS=(
        runs/benchmark_14b_batch_01
        runs/benchmark_14b_batch_02
        runs/benchmark_14b_batch_03
        runs/benchmark_14b_batch_04
        runs/benchmark_14b_batch_05
        runs/benchmark_14b_batch_06
        runs/benchmark_14b_batch_07
        runs/benchmark_14b_batch_08
        runs/benchmark_14b_batch_09
        runs/benchmark_14b_batch_10
        runs/benchmark_14b_retry_01
        runs/benchmark_14b_retry_02
        runs/benchmark_14b_retry_03
        runs/benchmark_14b_retry_04
    )

    python3 scripts/merge_apps_batches.py \
        --batch-dirs "${ALL_DIRS[@]}" \
        --output-dir "runs/benchmark_apps_14b_dual_unified"

    echo "✅ Benchmark run COMPLETE! Unified summary saved at runs/benchmark_apps_14b_dual_unified/summary.md"
else
    echo "⚠️  ${FAILED} batch(es) encountered issues. Inspect logs/."
fi
