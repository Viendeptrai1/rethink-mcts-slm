"""
Protocol v3.1 runner on Modal: one A100-40GB container that does what a Colab VM did
(deploy/colab/): vLLM 0.31.0 in a Python 3.13 system environment, the solver in a Python 3.11.17
venv, both on the same machine, driven by the frozen code's own setup.sh / serve.sh / run_plan.sh.

Runs are written to the Modal Volume `tlcn-v31-runs` (mounted at /vol, linked as /content/runs),
committed every few minutes, so a new call with the same plan resumes completed problems.
Logs go to /vol/logs/. The Hugging Face cache lives on the Volume `tlcn-hf-cache`.

  modal run deploy/modal_v31_runner.py::gpu_check                      # nvidia-smi + torch.cuda (cheap)
  modal run --detach deploy/modal_v31_runner.py::run --plan PLAN_FILE   # the real run (spends credit)
  modal run deploy/modal_v31_runner.py::status                          # progress, CPU only
  modal volume get tlcn-v31-runs runs/<run> ./somewhere                 # fetch results

The code shipped is colab_results/freeze/tlcn_v3.tar.gz: `git archive` of commit d9666c4 plus a
GIT_COMMIT file (the same archive the Colab runs used).
"""
import os
import shutil
import subprocess
import threading
import time
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "colab_results/freeze/tlcn_v3.tar.gz"

app = modal.App("tlcn-v31-runner")
runs_vol = modal.Volume.from_name("tlcn-v31-runs", create_if_missing=True)
hf_vol = modal.Volume.from_name("tlcn-hf-cache", create_if_missing=True)

image = (
    # CUDA toolkit (nvcc) is needed: FlashInfer JIT-compiles its top-k/top-p sampling kernel at
    # vLLM startup, as on the Colab VM (which ships /usr/local/cuda). torch is cu130, so CUDA 13.0.
    modal.Image.from_registry("nvidia/cuda:13.0.1-devel-ubuntu24.04", add_python="3.13")
    .apt_install("curl", "procps", "git")
    .env({"CUDA_HOME": "/usr/local/cuda"})
    # latest uv from the official installer (the PyPI mirror's uv did not know CPython 3.11.17)
    .run_commands("curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh",
                  "uv --version")
    # same install as deploy/colab/setup.sh: vLLM into the system Python, uv-managed Python 3.11.17
    .run_commands("uv pip install --system vllm==0.31.0", "uv python install 3.11.17")
    .env({"VLLM_LOGGING_LEVEL": "INFO", "HF_HOME": "/root/.cache/huggingface"})
    .add_local_file(str(ARCHIVE), "/opt/tlcn_v3.tar.gz", copy=True)
)

# Modal may serve an A100-40GB request on an A100-SXM4-80GB (no way to pin 40GB). run() then caps
# vLLM at 0.45 x 80 GB = 36 GB, the same memory budget as 0.90 x 40 GB on Colab, so the KV cache
# size (and with it scheduling) matches; same SM80 kernels either way.
# 12 vCPU and 83 GB RAM like the Colab A100 VM (32 GB was not enough: vLLM died during Qwen3.5 init).
GPU_KW = dict(image=image, gpu=os.environ.get("TLCN_GPU", "A100-40GB"), cpu=12, memory=83 * 1024)
COLAB_VLLM_BUDGET_GB = 0.90 * 40


@app.function(**GPU_KW, timeout=600)
def gpu_check():
    out = subprocess.run("nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader; "
                         "nvcc --version | tail -1; python3 -c \"import torch, vllm, sys; print('torch', torch.__version__, 'cuda', torch.version.cuda, "
                         "'available', torch.cuda.is_available(), 'vllm', vllm.__version__, 'python', sys.version.split()[0])\"; nproc; free -g | head -2",
                         shell=True, capture_output=True, text=True)
    print(out.stdout, out.stderr[-2000:])


def _sync_logs(stop: threading.Event, every: int = 240):
    logs = Path("/vol/logs")
    logs.mkdir(parents=True, exist_ok=True)

    def once():
        for f in Path("/content").glob("*.log"):
            shutil.copy2(f, logs / f.name)
        for marker in ("QUEUE_DONE", "QUEUE_FAILED"):
            if Path("/content", marker).exists():
                shutil.copy2(Path("/content", marker), logs / marker)
        try:
            runs_vol.commit()
            hf_vol.commit()
        except Exception as exc:  # a failed commit is retried on the next tick
            print("commit failed:", exc)

    while not stop.wait(every):
        once()
    once()  # final sync after run_plan.sh has exited (failure lines included)


@app.function(**GPU_KW, timeout=24 * 3600,
              volumes={"/vol": runs_vol, "/root/.cache/huggingface": hf_vol})
def run(plan_text: str):
    content = Path("/content")
    (content / "tlcn").mkdir(parents=True, exist_ok=True)
    subprocess.run(["tar", "xzf", "/opt/tlcn_v3.tar.gz", "-C", "/content/tlcn"], check=True)
    Path("/vol/runs").mkdir(parents=True, exist_ok=True)
    if not (content / "runs").exists():
        os.symlink("/vol/runs", "/content/runs")
    for marker in ("QUEUE_DONE", "QUEUE_FAILED"):
        Path("/vol/logs", marker).unlink(missing_ok=True)
    name, mem_mib = subprocess.run("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits",
                                   shell=True, capture_output=True, text=True).stdout.strip().split(", ")
    os.environ["EXPECTED_GPU"] = name  # setup.sh refuses any GPU other than EXPECTED_GPU
    if not name.startswith("NVIDIA A100-SXM4"):
        raise RuntimeError(f"unexpected GPU {name}")
    util = round(min(0.90, COLAB_VLLM_BUDGET_GB * 1024 / float(mem_mib)), 2)
    if util < 0.90:  # appended after serve.sh's own --gpu-memory-utilization 0.90, so it wins
        plan_text = "\n".join(l + f" --gpu-memory-utilization {util}" if l.startswith("serve ") else l
                              for l in plan_text.splitlines()) + "\n"
    Path("/vol/logs").mkdir(parents=True, exist_ok=True)
    with open("/vol/logs/modal_runtime.log", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} gpu={name} mem_mib={mem_mib} vllm_util={util}\n")
    print(f"GPU {name} ({mem_mib} MiB): vLLM memory utilization {util}")
    (content / "plan.txt").write_text(plan_text)
    stop = threading.Event()
    syncer = threading.Thread(target=_sync_logs, args=(stop,), daemon=True)
    syncer.start()
    rc = subprocess.call(["bash", "/content/tlcn/deploy/colab/run_plan.sh", "/content/plan.txt"])
    stop.set()
    syncer.join()
    print("run_plan exit", rc, "QUEUE_DONE" if (content / "QUEUE_DONE").exists() else "not done")
    return rc


@app.function(image=image, volumes={"/vol": runs_vol}, timeout=300)
def status():
    runs_vol.reload()
    for d in sorted(Path("/vol/runs").glob("*")):
        done = len(list(d.glob("problems/*/completed.json")))
        errs = len(list(d.glob("problems/*/error.json")))
        print(f"{d.name}: {done} completed, {errs} errors")
    q = Path("/vol/logs/queue.log")
    print(q.read_text()[-1500:] if q.exists() else "no queue.log yet")


@app.local_entrypoint()
def main(plan: str = ""):
    if plan:
        print(run.remote(Path(plan).read_text()))
