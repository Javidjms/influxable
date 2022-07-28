FROM python:3.9.2-buster
ENV PYTHONUNBUFFERED 1
ARG ENV

RUN apt-get update && apt-get install -y \
  gcc \
  musl-dev \
  build-essential \
  pkg-config

RUN mkdir /app/
WORKDIR /app/
COPY requirements.txt /app/requirements.txt
COPY requirements-dev.txt /app/requirements-dev.txt

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY . /app/

CMD tail -f /dev/null
