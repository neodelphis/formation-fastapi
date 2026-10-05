# syntax=docker/dockerfile:1.6

# --------------------------------------------------------------- #
# Image de build : installe les dépendances dans un venv isolé
# --------------------------------------------------------------- #
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Installation des dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python dans un venv
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

# --------------------------------------------------------------- #
# Image runtime : minimale, sans compilateur
# --------------------------------------------------------------- #
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOME=/app

# Copie du venv depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR ${APP_HOME}

# Copie du code applicatif
COPY --chown=appuser:appuser . ${APP_HOME}

USER appuser

EXPOSE 8000

# Healthcheck : interroge /health toutes les 30s
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request, sys; urllib.request.urlopen('http://127.0.0.1:8000/health').read(); sys.exit(0)" || exit 1

# Uvicorn derrière --proxy-headers (utile si reverse-proxy nginx devant)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
