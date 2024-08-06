FROM python:3.12-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl=7.74.* \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    # Poetry variables
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.3

# Install poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -
RUN curl --version
RUN curl -sSL "https://install.python-poetry.org" -o install-poetry.py \
    && python install-poetry.py \
    && rm install-poetry.py

ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry install -v --no-root --no-ansi

COPY . .

VOLUME /home/lottery/data/