FROM python:3

RUN mkdir -p /usr/local/registration/
COPY ./ /usr/local/registration/

RUN cd /usr/local/registration/ && python setup.py install

RUN useradd -m registration
USER registration

WORKDIR /home/registration/
