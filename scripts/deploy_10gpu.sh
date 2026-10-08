#!/usr/bin/env bash
# =============================================================================
# deploy_10gpu.sh
# Deploy 10 vLLM instances across 4 Modal accounts (viengemini excluded).
#
# Account allocation:
#   phanquocvien-123   → 3 GPUs (rethink-vllm-a, b, c)
#   kotorikotorii0     → 3 GPUs (rethink-vllm-a, b, c)
#   phanquocvien-1234  → 2 GPUs (rethink-vllm-a, b)
#   vienphanquoc-123   → 2 GPUs (rethink-vllm-a, b)
#
# Usage:
#   bash scripts/deploy_10gpu.sh [--model Qwen/Qwen2.5-Coder-14B-Instruct] [--gpu H200]
# =============================================================================

set -euo pipefail

MODEL="${VLLM_MODEL_ID:-Qwen/Qwen2.5-Coder-14B-Instruct}"
GPU="${VLLM_GPU:-H200}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }

mkdir -p logs/deploy

PIDS=()
NAMES=()

deploy_instance() {
  local profile="$1"
  local app_name="$2"
  local log_file="logs/deploy/${profile}_${app_name}.log"
  log "Deploying $app_name on profile $profile (log: $log_file)..."
  (
    MODAL_PROFILE="$profile" \
    MODAL_APP_NAME="$app_name" \
    VLLM_MODEL_ID="$MODEL" \
    VLLM_GPU="$GPU" \
      modal deploy deploy/modal_vllm.py > "$log_file" 2>&1
  ) &
  PIDS+=($!)
  NAMES+=("${profile}/${app_name}")
}

# ── phanquocvien-123: 4 instances ───────────────────────────────────────────
deploy_instance "phanquocvien-123" "rethink-vllm-a"
deploy_instance "phanquocvien-123" "rethink-vllm-b"
deploy_instance "phanquocvien-123" "rethink-vllm-c"
deploy_instance "phanquocvien-123" "rethink-vllm-d"

# ── kotorikotorii0: 3 instances ─────────────────────────────────────────────
deploy_instance "kotorikotorii0" "rethink-vllm-a"
deploy_instance "kotorikotorii0" "rethink-vllm-b"
deploy_instance "kotorikotorii0" "rethink-vllm-c"

# ── vienphanquoc-123: 3 instances ───────────────────────────────────────────
deploy_instance "vienphanquoc-123" "rethink-vllm-a"
deploy_instance "vienphanquoc-123" "rethink-vllm-b"
deploy_instance "vienphanquoc-123" "rethink-vllm-c"

log "Waiting for all 10 deployments to complete..."
FAIL=0
for i in "${!PIDS[@]}"; do
  pid="${PIDS[$i]}"
  name="${NAMES[$i]}"
  if wait "$pid"; then
    log "  ✅ Deployed: $name"
  else
    log "  ❌ Failed: $name (check logs/deploy/$(echo $name | tr / _).log)"
    FAIL=$((FAIL + 1))
  fi
done

if [ "$FAIL" -gt 0 ]; then
  log "⚠️  $FAIL deployment(s) failed."
  exit 1
fi
log "✅ All 10 GPU instances deployed successfully."
log ""
log "Expected endpoints:"

declare -A SLOTS=(
  [phanquocvien-123]="rethink-vllm-a rethink-vllm-b rethink-vllm-c"
  [kotorikotorii0]="rethink-vllm-a rethink-vllm-b rethink-vllm-c"
  [phanquocvien-1234]="rethink-vllm-a rethink-vllm-b"
  [vienphanquoc-123]="rethink-vllm-a rethink-vllm-b"
)

for profile in "${!SLOTS[@]}"; do
  for app in ${SLOTS[$profile]}; do
    echo "  https://${profile}--${app}-serve.modal.run/v1"
  done
done
