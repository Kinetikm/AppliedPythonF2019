FROM python:3.6-alpine3.7
COPY . /flights
WORKDIR /flights
ENV FLASK_CONFIG config.py
RUN apk --no-cache add mariadb-dev build-base bash musl-dev linux-headers
RUN pip3 install -r requirements.txt