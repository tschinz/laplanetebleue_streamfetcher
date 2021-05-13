#!/bin/bash

set -e # exit on any error

# launch at starup the scripts
python /usr/src/app/index.py -av -o /data

# start cronjob in foreground mode
cron -f

# all after cron -f is not used only for future references
tail -f /dev/null