#!/bin/bash
# Prepare a fresh Colab runtime: check the GPU, install vLLM (system Python) and the project
# (Python 3.11 venv, required for correct tracing), then run the offline test suite.
set -euo pipefail
EXPECTED_GPU="${EXPECTED_GPU:-NVIDIA A100-SXM4-40GB}"
GPU=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
if [ "$GPU" != "$EXPECTED_GPU" ]; then echo "SETUP_FAILED: GPU is '$GPU', expected '$EXPECTED_GPU'"; exit 1; fi
UV_SYSTEM_PYTHON=true uv pip install "vllm==0.31.0"
python3 -c "import vllm, sys; assert vllm.__version__ == '0.31.0', vllm.__version__; print('vllm', vllm.__version__, 'python', sys.version.split()[0])"
UV_SYSTEM_PYTHON=false uv venv /content/py311 --python 3.11.17
# Pinned to the versions recorded in the pilot manifests, so a later session reproduces the same
# runtime fingerprint and can resume a run.
UV_SYSTEM_PYTHON=false uv pip install --python /content/py311/bin/python -e "/content/tlcn[dev]" \
  pydantic==2.14.3 jinja2==3.1.6 requests==2.34.2 pyyaml==6.0.3
cd /content/tlcn
/content/py311/bin/python -m pytest -q -p no:cacheprovider \
  --deselect tests/acceptance/test_scenario_c.py \
  --deselect tests/integration/test_research_foundation.py::test_docker_real_container_execution_and_trace
echo "SETUP_OK gpu=$GPU commit=$(cat /content/tlcn/GIT_COMMIT 2>/dev/null)"
