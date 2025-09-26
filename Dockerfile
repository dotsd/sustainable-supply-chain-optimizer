# Sustainable Supply Chain Optimizer - Container Image
# Lightweight Python image
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app

WORKDIR ${APP_HOME}

# System deps (if any future native libs needed, add here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates build-essential git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement spec first for layer caching
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Environment defaults (override in runtime environment / orchestrator)
ENV AWS_REGION=us-east-1 \
    PYTHONPATH=/app \
    USE_AWS_AGENTCORE=0 \
    FLASK_ENV=production

# Health check script (simple)
RUN printf '#!/usr/bin/env bash\nset -e\ncurl -fsS http://localhost:5000/health >/dev/null || exit 1\n' > /healthcheck.sh \
    && chmod +x /healthcheck.sh

# Use gunicorn for production serving of Flask API; fall back to simple server if missing
RUN pip install gunicorn

# Default command: start API endpoint (Flask app)
# api_endpoint.py defines app = Flask(__name__)
CMD ["gunicorn", "api_endpoint:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120"]

# For local debug you can override CMD with: python api_endpoint.py
