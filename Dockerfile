FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-interaction --no-ansi

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY app.py ./

ENV PATH="/app/.venv/bin:$PATH"
# Default model (can be overridden)
ENV MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]