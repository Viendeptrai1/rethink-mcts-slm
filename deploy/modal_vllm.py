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
import subprocess
import modal

APP_NAME = os.environ.get("MODAL_APP_NAME", "rethink-vllm")
MODEL_ID = os.environ.get("VLLM_MODEL_ID", "Qwen/Qwen2.5-Coder-14B-Instruct")
GPU_TYPE = os.environ.get("VLLM_GPU", "H200")  # H200, H100, A100-80GB, A10G
MAX_MODEL_LEN = int(os.environ.get("VLLM_MAX_MODEL_LEN", "16384"))
IDLE_SCALEDOWN_SECONDS = 300  # Auto-shutdown after 5 minutes of inactivity to save costs

# 2. Container Environment & Persistent Cache
app = modal.App(APP_NAME)
hf_cache_volume = modal.Volume.from_name("rethink-hf-cache", create_if_missing=True)

vllm_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "vllm>=0.6.3",
        "huggingface_hub",
        "fastapi",
    )
    .env({
        "VLLM_USE_FLASHINFER_SAMPLER": "0",
        "VLLM_LOGGING_LEVEL": "INFO",
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
        "--enforce-eager",
    ]
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
