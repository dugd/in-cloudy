FROM python:3.13-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/var/cache/pypoetry \
    POETRY_HOME=/usr/local \
    POETRY_VERSION=2.1.4

ENV PATH="$POETRY_HOME/bin:/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
