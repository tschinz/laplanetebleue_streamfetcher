FROM python:3.8-slim AS runtime-image
MAINTAINER tschinz

# Update and install git
RUN apt-get update && apt-get install -y --no-install-recommends git cron

# Create and install crontab
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab &&\
    crontab /etc/cron.d/crontab

ARG dest=/usr/src/app

# Create the application directories
RUN mkdir $dest
WORKDIR $dest
RUN mkdir ./src
RUN mkdir /data

# Copy the rest of the codebase into the image
COPY src/ ./src
COPY index.py .
COPY condaenv.yml /tmp/
COPY requirements.txt /tmp/

# Install python environment
RUN pip install -r /tmp/requirements.txt
#RUN conda env create -f /tmp/condaenv.yml

RUN echo "conda activate laplanetebleue-env" >> ~/.bashrc

## set environment variables

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#EXPOSE 5000

CMD [python /usr/src/app/index.py -a -v -o /data]
