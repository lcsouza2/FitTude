FROM python:3.13-alpine AS builder

RUN apk add --no-cache build-base libffi-dev
RUN pip install --no-cache-dir poetry

WORKDIR /build

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root



FROM python:3.13-alpine AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -D appuser

RUN mkdir /api && chown appuser:appgroup /api

WORKDIR /api

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --chown=appuser:appgroup . .

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]