FROM python:3.7
FROM tiangolo/meinheld-gunicorn:python3.7

RUN mkdir /code
WORKDIR /code
COPY ./flights .
COPY ./models ./models
RUN pip install -r requirements.txt
