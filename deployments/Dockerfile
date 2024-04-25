FROM python:3.11.5-slim-bookworm

ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /lazysplit
COPY poetry.lock pyproject.toml /lazysplit/

RUN poetry install --no-interaction --no-cache --without dev

COPY src/ /lazysplit/src/
COPY static /lazysplit/static/

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "python", "src/main.py"]
