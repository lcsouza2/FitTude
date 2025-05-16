# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y curl build-essential

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adicionar Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Copiar apenas os arquivos de dependência para instalar mais rápido (cache)
COPY pyproject.toml poetry.lock* ./

# Instalar dependências do projeto (sem ambiente virtual)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copiar o restante do código
COPY . .

# Expor a porta
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:MAIN_APP", "--host", "0.0.0.0", "--port", "8000", "--reload"]
