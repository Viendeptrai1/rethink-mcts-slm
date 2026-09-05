# Dockerfile for isolated RethinkMCTS worker (§10.1)
FROM python:3.11-slim

# Create unprivileged non-root user
RUN groupadd -g 1000 sandboxgroup && \
    useradd -u 1000 -g sandboxgroup -s /bin/bash -m sandboxuser

WORKDIR /workspace
RUN chown sandboxuser:sandboxgroup /workspace

USER sandboxuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python3"]
