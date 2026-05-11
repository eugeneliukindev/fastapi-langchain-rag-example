FROM python:3.13-slim AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./

FROM base AS migrate
RUN uv export --frozen --only-group migrations --no-hashes | uv pip install --system -r -
COPY migrations/ ./migrations/
COPY src/core/db/ ./src/core/db/
CMD ["alembic", "upgrade", "head"]

FROM base AS app
RUN uv export --frozen --no-default-groups --no-hashes | uv pip install --system -r -
COPY src/ ./src/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
