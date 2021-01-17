FROM python:3.8-alpine

RUN adduser -D stationboard

WORKDIR /usr/src/stationboard

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
# COPY migrations migrations
COPY stationboard.py .env config.py start.sh ./
RUN chmod +x start.sh

ENV FLASK_APP stationboard.py
ENV FLASK_ENV development

RUN chown -R stationboard:stationboard ./
USER stationboard

EXPOSE 5000

ENTRYPOINT ["./start.sh"]