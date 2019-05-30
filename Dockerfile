# Created by Maximillian M. Estrada on 30-May-2019

# Dockerfile to build Dengun Exam

# Use an official Python 3 runtime as our base image
FROM python:3.7

MAINTAINER maxestrada

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# Install any needed packages specified in our `requirements.txt`
RUN pip install -r requirements.txt

# Set the working directory to `/dengun_crm`
WORKDIR /dengun_crm

# Copy the application directory contents into the container at `/dengun_crm`
COPY ./src/dengun_crm /dengun_crm
