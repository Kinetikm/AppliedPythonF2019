FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /flight_service

WORKDIR /flight_service

ADD . /flight_service

RUN pip install -r requirments.txt
