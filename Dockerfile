FROM python:3.11-slim-buster

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]
