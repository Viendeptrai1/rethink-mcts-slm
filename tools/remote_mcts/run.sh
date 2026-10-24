#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

if ! command -v docker >/dev/null 2>&1 || ! docker info >/dev/null 2>&1; then
  echo "Docker daemon is unavailable; refusing to execute generated code on the host." >&2
  exit 1
fi

mkdir -p outputs/rethinkmcts outputs/rethinkmcts_attempts outputs/benchmarks outputs/remote_mcts
if [[ "$(id -u)" == "0" ]]; then
  chown -R 10001:10001 outputs
fi

docker build -t rethinkmcts-gpu:local tools/remote_mcts
image_id="$(docker image inspect -f '{{.Id}}' rethinkmcts-gpu:local)"
echo "MCTS image: $image_id"

# Host networking reaches Ollama even when it listens only on host loopback.
docker run --rm \
  --network host \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 128 \
  --cpus 4 \
  --memory 12g \
  --tmpfs /tmp:rw,nosuid,nodev,size=2g \
  --user 10001:10001 \
  --env LLM_PROVIDER=ollama \
  --env LLM_BASE_URL=http://127.0.0.1:11434/v1 \
  --env LLM_API_KEY=ollama \
  --env "RETHINKMCTS_IMAGE_ID=$image_id" \
  --mount "type=bind,src=$PWD,dst=/workspace,readonly" \
  --mount "type=bind,src=$PWD/outputs,dst=/workspace/outputs" \
  rethinkmcts-gpu:local "$@" 2>&1 | tee -a outputs/remote_mcts/worker.log
