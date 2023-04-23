FROM python:3.10-slim

WORKDIR /code

ENV PYTHONUNBUFFERED=1  \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.2.2 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \  
  && apt-get install -y --no-install-recommends build-essential libpq-dev \  
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi 

COPY src /code

CMD [ "python", "run.py"]