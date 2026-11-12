#!/bin/bash
# usage: serve.sh <hf-model-id> <short-name> [extra vllm args...]
# Stops any running vLLM, starts the model detached, waits up to 30 min for /health.
MODEL=$1; NAME=$2; shift 2
pkill -f "[v]llm serve" || true
for i in $(seq 1 30); do pgrep -f "[v]llm serve" >/dev/null || break; sleep 2; done
setsid nohup vllm serve "$MODEL" --host 127.0.0.1 --port 8000 --dtype bfloat16 --max-model-len 32768 \
  --gpu-memory-utilization 0.90 --seed 0 "$@" < /dev/null > /content/vllm_$NAME.log 2>&1 &
for i in $(seq 1 180); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/health)" = "200" ] && { echo "SERVE_OK $MODEL"; exit 0; }
  pgrep -f "[v]llm serve" >/dev/null || { echo "SERVE_FAILED: vLLM exited"; tail -20 /content/vllm_$NAME.log; exit 1; }
  sleep 10
done
echo "SERVE_FAILED: no /health after 30 min"; exit 1
