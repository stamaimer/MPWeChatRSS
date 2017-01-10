#!/usr/bin/env bash
# start.sh

# celery -A celary.celery worker -B -l info

gunicorn -w 1 -k gevent run:app -p app.pid -b 127.0.0.1:6666 --log-level=DEBUG
