FROM python:3.7.6-slim-buster

ENV PATH /usr/local/bin:$PATH

COPY . /app

WORKDIR /app

ENV LANG C.UTF-8

ENV PYTHON_VERSION 3.7.6

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
