FROM python:3.10-slim AS base

WORKDIR /app

RUN apt update && apt install -y libgl1 libglib2.0-0 make && \
    rm -rf /var/lib/apt/lists/*

COPY requirements/requirements-base.txt /app/requirements/
RUN pip install --no-cache-dir -r requirements/requirements-base.txt

ENV PYTHONPATH=.


FROM base AS base-dev

COPY requirements/requirements-dev.txt /app/requirements/
RUN pip install --no-cache-dir -r requirements/requirements-dev.txt


FROM base AS prod

COPY . .

RUN rm -rf /app/tests /app/requirements/requirements-dev.txt requirements/requirements-dvc.txt


FROM base-dev AS dev

COPY . .
