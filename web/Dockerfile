FROM python:3.7-slim

RUN mkdir -p /var/www/app
WORKDIR /var/www/app
ADD . /var/www/app/

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .
