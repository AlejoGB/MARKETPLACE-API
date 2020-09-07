FROM python:3.8.5-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /backend-api
WORKDIR /backend-api
COPY . /backend-api

RUN adduser -D admin
USER admin
