FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY src ./src

FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home appuser

WORKDIR /app

COPY --from=builder --chown=appuser:appuser /app/.venv ./.venv
COPY --from=builder --chown=appuser:appuser /app/src ./src

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD curl -fsS http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "src.app.api:app", "--host", "0.0.0.0", "--port", "8000"]
