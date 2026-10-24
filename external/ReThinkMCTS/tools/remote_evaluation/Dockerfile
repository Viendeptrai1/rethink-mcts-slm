FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_DATASETS_OFFLINE=1 \
    HF_HOME=/tmp/huggingface \
    HOME=/tmp

COPY requirements.txt /tmp/evaluation-requirements.txt
RUN pip install --no-cache-dir -r /tmp/evaluation-requirements.txt

WORKDIR /workspace
USER 10001:10001
ENTRYPOINT ["python", "-m", "tools.remote_evaluation.run_bundle"]
