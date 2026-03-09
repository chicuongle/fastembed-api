FROM python:3.10-slim

ARG MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
ENV MODEL_NAME=$MODEL_NAME

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

COPY app.py ./

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]