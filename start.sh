#!/bin/sh
source venv/bin/activate

export FLASK_APP=stationboard.py
export FLASK_ENV=development

exec gunicorn -b :5000 --access-logfile - --error-logfile - stationboard:app