FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

COPY pyproject.toml uv.lock* ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.14.2-slim

RUN groupadd --system --gid 999 user && \
    useradd --system --gid 999 --uid 999 --create-home user

COPY --from=builder --chown=user:user /app/.venv /app/.venv
COPY --from=builder --chown=user:user /app/backend /app/backend
COPY --from=builder --chown=user:user /app/pyproject.toml /app/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER user
EXPOSE 7000
ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["uvicorn", "backend.kanban.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "7000"]