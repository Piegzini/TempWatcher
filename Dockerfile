FROM python:3.10-alpine

WORKDIR /usr/src/tempwatcher
COPY requirements.txt ./

RUN pip install requirements.txt

COPY main.py ./


