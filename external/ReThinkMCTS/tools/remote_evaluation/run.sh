#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

if ! command -v docker >/dev/null 2>&1 || ! docker info >/dev/null 2>&1; then
  echo "Docker daemon is unavailable. Do not run untrusted candidate code directly on the host." >&2
  exit 1
fi

mkdir -p outputs/remote_evaluation
if [[ "$(id -u)" == "0" ]]; then
  chown -R 10001:10001 outputs
fi

docker build -t rethinkmcts-evaluation:local tools/remote_evaluation
image_id="$(docker image inspect -f '{{.Id}}' rethinkmcts-evaluation:local)"
echo "Evaluation image: $image_id"

docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 128 \
  --cpus 4 \
  --memory 12g \
  --tmpfs /tmp:rw,nosuid,nodev,size=2g \
  --user 10001:10001 \
  --env "EVALUATION_IMAGE_ID=$image_id" \
  --env EVALUATION_BACKEND=docker \
  --env EVALUATION_CPU_LIMIT=4 \
  --env EVALUATION_MEMORY_LIMIT=12g \
  --env EVALUATION_PIDS_LIMIT=128 \
  --mount "type=bind,src=$PWD,dst=/workspace,readonly" \
  --mount "type=bind,src=$PWD/outputs,dst=/workspace/outputs" \
  rethinkmcts-evaluation:local "$@" 2>&1 | tee -a outputs/remote_evaluation/worker.log
