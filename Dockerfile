FROM python:3.10-slim

WORKDIR /usr/src/tempwatcher
COPY requirements.txt ./

RUN pip install requirements.txt

COPY main.py ./

CMD ["python3", "./main.py"]

