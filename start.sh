#!/bin/sh
source venv/bin/activate

export FLASK_APP=stationboard.py
export FLASK_ENV=development
export FLASK_DEBUG=1

exec gunicorn -b :5000 --access-logfile - --error-logfile - stationboard:app