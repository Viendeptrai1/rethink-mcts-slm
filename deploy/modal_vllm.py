"""
Modal vLLM Deployment for RethinkMCTS.
Deploys an OpenAI-compatible vLLM inference server on high-performance GPUs (H200 / H100).

Usage:
  # Deploy persistently to Modal (generates permanent web URL):
  modal deploy deploy/modal_vllm.py

  # Or run ephemerally for an interactive session:
  modal run deploy/modal_vllm.py
"""

import os
import shlex
import subprocess
import modal

APP_NAME = os.environ.get("MODAL_APP_NAME", "rethink-vllm")
MODEL_ID = os.environ.get("VLLM_MODEL_ID", "Qwen/Qwen2.5-Coder-14B-Instruct")
GPU_TYPE = os.environ.get("VLLM_GPU", "L40S")  # L40S ($1.95/hr, 48GB VRAM), H200, A100-80GB
MAX_MODEL_LEN = int(os.environ.get("VLLM_MAX_MODEL_LEN", "16384"))
IDLE_SCALEDOWN_SECONDS = int(os.environ.get("MODAL_IDLE_SECONDS", "180"))  # Auto-shutdown after 3 mins of inactivity
# Default "1" reproduces the original 14B runs; "0" enables CUDA graphs (faster decode).
ENFORCE_EAGER = os.environ.get("VLLM_ENFORCE_EAGER", "1") != "0"
# Requests one container accepts at once; vLLM batches them. The original runs sent 1 at a time.
MAX_CONCURRENT_INPUTS = int(os.environ.get("MODAL_MAX_INPUTS", "32"))
# Extra `vllm serve` flags for a specific model, e.g. "--dtype bfloat16 --seed 0".
EXTRA_ARGS = os.environ.get("VLLM_EXTRA_ARGS", "")

# 2. Container Environment & Persistent Cache
app = modal.App(APP_NAME)
hf_cache_volume = modal.Volume.from_name("rethink-hf-cache", create_if_missing=True)

vllm_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        # The Oct 2026 14B APPS runs resolved this to vllm 0.31.0; pin it with VLLM_PIP_SPEC=vllm==0.31.0.
        os.environ.get("VLLM_PIP_SPEC", "vllm>=0.6.3"),
        "huggingface_hub",
        "fastapi",
    )
    .env({
        "VLLM_USE_FLASHINFER_SAMPLER": "0",
        "VLLM_LOGGING_LEVEL": "INFO",
        # Bake the launch settings so the container sees the values chosen at deploy time.
        "VLLM_MODEL_ID": MODEL_ID,
        "VLLM_MAX_MODEL_LEN": str(MAX_MODEL_LEN),
        "VLLM_ENFORCE_EAGER": "1" if ENFORCE_EAGER else "0",
        "VLLM_EXTRA_ARGS": EXTRA_ARGS,
    })
)


# 3. vLLM OpenAI-Compatible Web Server
@app.function(
    image=vllm_image,
    gpu=GPU_TYPE,
    scaledown_window=IDLE_SCALEDOWN_SECONDS,
    volumes={"/root/.cache/huggingface": hf_cache_volume},
    timeout=1800,
    startup_timeout=600,
    cpu=4.0,
    memory=32768,  # 32GB system RAM
    max_containers=1,
)
@modal.concurrent(max_inputs=MAX_CONCURRENT_INPUTS)
@modal.web_server(port=8000, startup_timeout=600)
def serve():
    """
    Launches vLLM OpenAI-compatible server on internal port 8000.
    Modal automatically proxies this port to the external HTTPS endpoint.
    """
    cmd = [
        "vllm", "serve", MODEL_ID,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--gpu-memory-utilization", "0.90",
        "--max-model-len", str(MAX_MODEL_LEN),
        "--trust-remote-code",
    ]
    if ENFORCE_EAGER:
        cmd.append("--enforce-eager")
    cmd.extend(shlex.split(EXTRA_ARGS))
    print(f"Starting vLLM server with command: {' '.join(cmd)}")
    subprocess.Popen(cmd)


@app.local_entrypoint()
def main():
    print("=" * 60)
    print(f"RethinkMCTS vLLM Server on Modal")
    print(f"Model: {MODEL_ID}")
    print(f"GPU: {GPU_TYPE}")
    print(f"Auto-scaledown idle window: {IDLE_SCALEDOWN_SECONDS}s")
    print("=" * 60)
    print("To deploy permanent endpoint, run:")
    print("  modal deploy deploy/modal_vllm.py")
    print("=" * 60)
