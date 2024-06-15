FROM python:3.12-alpine

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt
  
