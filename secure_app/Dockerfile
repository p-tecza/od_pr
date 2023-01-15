# syntax=docker/dockerfile:1

FROM python:alpine

WORKDIR /python-docker

COPY pip-install/libraries requirements.txt
RUN pip3 install -r requirements.txt
RUN apk add openssl
COPY . .

CMD openssl genrsa -des3 -out server.key 2048 ; openssl req -new -key server.key -out server.csr ; \
cp server.key server.key.org ; openssl rsa -in server.key.org -out server.key ; \
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt; \
python3 application.py

