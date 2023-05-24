FROM python:3.10

RUN apt-get update && apt-get install -y cron

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_ENV=dev
ENV FLASK_APP=app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 5000
