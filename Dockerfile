FROM python:3.8.5-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev    
RUN apk add --update --no-cache postgresql-client
RUN apk add libjpeg zlib-dev jpeg-dev 

RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps 

RUN mkdir /backend-api
WORKDIR /backend-api
COPY . /backend-api

RUN adduser -D admin
USER admin
