FROM python:3

RUN mkdir -p /usr/local/auth/
COPY ./ /usr/local/auth/

RUN cd /usr/local/auth/ && python setup.py install

RUN useradd -m auth
USER auth

WORKDIR /home/auth/
