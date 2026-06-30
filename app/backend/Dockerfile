# syntax=docker/dockerfile:1
# --- Image de base commune ---
FROM python:3.11-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app

# --- Dépendances ---
FROM base AS deps
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# --- Image finale (non-root, minimale) ---
FROM base AS runtime
# Utilisateur non privilégié (sécurité)
RUN useradd --create-home --uid 10001 appuser
COPY --from=deps /install /usr/local
COPY app ./app
USER appuser
EXPOSE 8000
# Sonde de santé intégrée à l'image
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://localhost:8000/healthz').status==200 else sys.exit(1)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
