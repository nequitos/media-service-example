
FROM debian:bullseye AS Linux

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y ca-certificates
RUN #apt-get install -y postgres-common
RUN #su && su -l postgres && initdb -D /var/lib/postgres/data && exit

FROM python:3.13.2-bullseye AS Python
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /usr/media-service-example
RUN echo "PATH=/usr/media-service-example/src" > /etc/environment

# Building python dependent packages
COPY requirements.txt /usr/media-service-example/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Сopy project to container
COPY src /usr/media-service-example/src
COPY init_db.py /usr/media-service-example
