FROM python:3.8-slim-buster

RUN apt-get update && apt-get install --yes libmagic-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD src/config/requirements/base.txt ./src/config/requirements.txt
RUN  python -m pip install -U pip && pip install -r src/config/requirements.txt
COPY . /usr/src/app

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
