#!/bin/bash
# usage: run_plan.sh <plan-file>
# Executes a plan line by line (kinds: serve, run, gate). Stops at the first serve/gate failure
# or when vLLM is down. A run whose exit code is non-zero (some problems errored) is resumed
# once; remaining per-problem errors are recorded, not fatal. Writes /content/QUEUE_DONE or
# /content/QUEUE_FAILED and packs results into /content/results.tar.gz.
PLAN=$1; LOG=/content/queue.log
stamp(){ echo "$(date -u +%FT%TZ) $*" >> $LOG; }
pack(){ cd /content && tar czf /content/results.tar.gz runs *.log 2>/dev/null; }
fail(){ stamp "FAILED $*"; echo "$*" > /content/QUEUE_FAILED; pack; exit 1; }
stamp "QUEUE_START commit=$(cat /content/tlcn/GIT_COMMIT 2>/dev/null)"
bash /content/tlcn/deploy/colab/setup.sh > /content/setup.log 2>&1 || fail "setup (see setup.log)"
stamp "SETUP_OK"
while IFS= read -r line; do
  case "$line" in ""|"#"*) continue;; esac
  eval set -- "$line"; kind=$1; shift
  stamp "START $line"
  case $kind in
    serve) bash /content/tlcn/deploy/colab/serve.sh "$@" >> $LOG 2>&1 || fail "serve $*";;
    gate)  (cd /content/tlcn && /content/py311/bin/python scripts/pilot_gate.py "$@" > /content/gate_$(basename "$1").log 2>&1) \
             || fail "gate $* (see gate_$(basename "$1").log)";;
    run)   name=$1; shift
           [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/health)" = "200" ] || fail "vLLM down before $name"
           for attempt in 1 2; do
             (cd /content/tlcn && /content/py311/bin/python scripts/run_benchmark_batch.py "$@" >> /content/$name.log 2>&1) && break
             stamp "RUN_NONZERO $name attempt $attempt"
             [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/health)" = "200" ] || fail "vLLM down during $name"
           done;;
    *) fail "unknown plan line: $line";;
  esac
  stamp "DONE $kind $1"
  pack
done < "$PLAN"
stamp "QUEUE_DONE"; pack; touch /content/QUEUE_DONE
