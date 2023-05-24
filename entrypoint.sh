#!/bin/bash

flask fab create-db

flask fab create-admin --username $ADMIN_USERNAME --firstname admin --lastname admin --email admin@fab.com --password $ADMIN_PASSWORD

flask retrive_update_wiki_data

if [[ "$FLASK_ENV" == "dev" ]]; then
    echo "Start dev server"
    flask run --reload -h "0.0.0.0" -p 5000 --debug
else
    echo "Start prod server"
    gunicorn -b 0.0.0.0:5000 --log-level INFO run:app
fi