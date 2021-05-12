########## 1st Stage ##########
FROM python:3.8-slim-buster AS build-image

# Update and install git
RUN apt-get update && apt-get install -y --no-install-recommends libcurl4-openssl-dev libssl-dev build-essential

# instead of installing, create wheels
RUN pip3 install --upgrade pip
COPY setup.py ./tmp
COPY src/ ./tmp/src
RUN pip3 wheel --wheel-dir=/tmp/wheels ./tmp

########## 2nd Stage ##########
FROM python:3.8-slim-buster AS runtime-image
MAINTAINER tschinz

RUN apt-get update && apt-get install -y --no-install-recommends cron libcurl4-openssl-dev libssl-dev

# Create and install crontab
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab &&\
    crontab /etc/cron.d/crontab

ARG dest=/usr/src/app

## copy wheels from build image and install packages from wheels
COPY --from=build-image /tmp/wheels /tmp/wheels

## Get all wheels and install them. We had to use '--no-deps' for our 'src' package because
## this latter needs git to install all its dependencies.
RUN WHEELS=$(cd /tmp/wheels; ls -1 *.whl | grep -v src | awk -F - '{ gsub("_", "-", $1); print $1 }' | uniq) && \
    pip3 install --no-index --find-links=/tmp/wheels $WHEELS && \
    pip3 install --no-index --find-links=/tmp/wheels src --no-deps

RUN rm -rf /tmp/wheels

# Create the application directories
RUN mkdir /data
RUN mkdir $dest
WORKDIR $dest

# Copy the rest of the codebase into the image
COPY index.py .

## set environment variables

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1



# Run command once at startup
CMD ["python", "/usr/src/app/index.py", "-av", "-o", "/data"]
# Dummy command to keep container in foreground and running
CMD ["tail", "-f", "/dev/null"]

# Setup entrypoint.sh
#COPY docker-entrypoint.sh /usr/local/bin/
#ENTRYPOINT ["docker-entrypoint.sh"]