FROM python:3.7.3
ENV PYTHONUNBUFFERED 1
ARG ENV

RUN apt-get update && apt-get install -y \
  gcc \
  musl-dev \
  build-essential \
  libssl-dev \
  libffi-dev \
  python3.5-dev \
  libldap2-dev \
  libsasl2-dev \
  libpq-dev

RUN mkdir /app/
WORKDIR /app/
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app/

CMD tail -f /dev/null
