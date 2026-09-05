"""
Kịch bản triển khai vLLM Server trên Cloud GPU bằng Modal Labs.
Hỗ trợ phục vụ các mô hình phân khúc <= 14B (như Qwen/Qwen2.5-Coder-7B-Instruct)
với giao thức tương thích OpenAI API (/v1/chat/completions).

Cách chạy:
1. modal setup (nếu chưa đăng nhập)
2. modal deploy models/modal_vllm.py (để deploy production)
   hoặc modal serve models/modal_vllm.py (để test live dev)
"""

import modal

MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
GPU_TYPE = "A10G"  # Có thể đổi thành "L4", "A100-40GB" tùy ngân sách

# Định nghĩa môi trường Image chứa vLLM
vllm_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "vllm>=0.6.0",
        "huggingface_hub",
        "torch"
    )
)

app = modal.App("qwen-coder-vllm")


@app.function(
    image=vllm_image,
    gpu=GPU_TYPE,
    timeout=600,
    container_idle_timeout=300,
    allow_concurrent_inputs=32
)
@modal.web_server(port=8000, startup_timeout=300)
def serve():
    import subprocess

    cmd = [
        "python3", "-m", "vllm.entrypoints.openai.api_server",
        "--model", MODEL_NAME,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--max-model-len", "8192",
        "--trust-remote-code",
        "--disable-log-requests"
    ]
    subprocess.Popen(cmd)
