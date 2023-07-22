FROM python:3.10.11-slim as builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir=/app/wheels -r ./requirements.txt


FROM python:3.10.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENGINE_PATH=/usr/games/stockfish

WORKDIR /app

# Я не знаю как правильно засунуть скачку стокфиша и либкаиро2 в билдера
RUN apt-get update && \
    apt-get install -y stockfish && \
    apt-get install -y libcairo2

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache --no-cache-dir /wheels/*

COPY ./src ./src
COPY ./templates ./templates
COPY ./README.md ./README.md

CMD ["python", "-m", "src"]