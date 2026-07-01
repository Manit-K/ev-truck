FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    unzip \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://sdk.cloud.google.com | bash

ENV PATH="/root/google-cloud-sdk/bin:${PATH}"