# Occupant Responsive Buildings
# https://github.com/cweyandt/orb
# Base docker image for running ORB framework
# Created 2020-06-16, cweyandt@berkeley.edu

# Initialize build on top of jupyterlab with tensorflow
# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/specifics.html#tensorflow
FROM jupyter/tensorflow-notebook

USER root

# Basic updating & utility installation
RUN apt update
RUN apt install -y wget unzip vim-tiny git

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Download ORB repository -- DO THIS IN DOCKER COMPOSE
# WORKDIR /home/jovyan
# RUN git clone https://github.com/cweyandt/orb.git


# Map local data directory -- IN DOCKER COMPOSE

