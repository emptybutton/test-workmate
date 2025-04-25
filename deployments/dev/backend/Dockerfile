FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS app

WORKDIR /app

ENV UV_LINK_MODE copy
ENV UV_PROJECT_ENVIRONMENT /run/app/.venv
ENV UV_CACHE_DIR /run/app/uv

ENV PYTHONPATH /app/src:/app/tests
ENV WATCHFILES_FORCE_POLLING true

ENTRYPOINT ["bash", "deployments/dev/backend/entrypoint.sh"]
