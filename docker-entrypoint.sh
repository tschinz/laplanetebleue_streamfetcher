#!/bin/bash

python /usr/src/app/index.py -av -o /data

cron -f
