FROM python:3.10-slim AS model-downloader

WORKDIR /app

RUN apt update && apt install -y openssh-client make git && \
    rm -rf /var/lib/apt/lists/*

ARG STAGING_HOST
ARG SSH_PRIVATE_KEY

RUN mkdir -p /root/.ssh && \
    echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa && \
    ssh-keyscan $STAGING_HOST >> /root/.ssh/known_hosts

COPY requirements/requirements-dvc.txt .
RUN pip install --no-cache-dir -r requirements-dvc.txt

COPY Makefile .env /app/

RUN mkdir -p /app/models && make dvc.get.files
RUN rm /root/.ssh/id_rsa


FROM python:3.10-slim AS base

WORKDIR /app

RUN apt update && apt install -y libgl1 libglib2.0-0 make && \
    rm -rf /var/lib/apt/lists/*

COPY requirements/requirements-base.txt /app/requirements/
RUN pip install --no-cache-dir -r requirements/requirements-base.txt


FROM base AS base-dev

COPY requirements/requirements-dev.txt /app/requirements/
RUN pip install --no-cache-dir -r requirements/requirements-dev.txt


FROM base AS prod

COPY . .
COPY --from=model-downloader /app/models /app/models

RUN rm -rf /app/tests /app/requirements/requirements-dev.txt requirements/requirements-dvc.txt


FROM base-dev AS dev

COPY . .
COPY --from=model-downloader /app/models /app/models
