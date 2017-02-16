#!/usr/bin/env bash
# start.sh

source ../venv/bin/activate

celery -A celary.celery worker -B -l info