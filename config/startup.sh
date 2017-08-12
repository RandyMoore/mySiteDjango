#!/usr/bin/env bash

# Perform 1 time actions at container startup

# Populate Postgres with schema and data
postgres_host=db
postgres_port=5432
max_poll=30

poll=0
while : ; do
    pg_isready -h $postgres_host -p $postgres_port
    if [ $? -eq 0 ]
    then
        echo "Postgres came up, whoo hoo"
        break
    fi
    echo "Postgres isn't up yet..."

    poll=$((poll+1))
    if [ $poll -gt $max_poll ]
    then
        echo "Postgres never came up - returning startup error"
        exit 1
    fi

    sleep 2
done

# Create DB Schema, load data from fixtures
cd /usr/local/src
./manage.py migrate --settings=my_site_django.prod_settings
