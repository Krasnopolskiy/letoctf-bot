FROM python:3.12

ENV PYTHONPATH /bot

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-cache

ADD bot bot

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
