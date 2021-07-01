# Occupant Responsive Buildings
# https://github.com/cweyandt/orb
# Base docker image for running ORB framework
# Created 2020-06-16, cweyandt@berkeley.edu

# Initialize build with 
# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/specifics.html#tensorflow
#FROM tensorflow/tensorflow:latest
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

MAINTAINER Chris Weyandt <cweyandt@berkeley.edu>

# Basic updating & utility installation
#RUN apt update
#RUN apt install -y \
#	wget \
#	unzip \
#	vim-tiny \
#	git

#RUN python3 -m pip --no-cache-dir install --upgrade \
#    "pip<20.3" \
#    setuptools

RUN /usr/local/bin/python -m pip install --upgrade pip

# RUN npm install -g swagger-spec-to-pdf

COPY docker/orb.requirements.txt requirements.txt
COPY docker/orb.gunicorn_conf.py /gunicorn_conf.py
RUN pip install -r requirements.txt



