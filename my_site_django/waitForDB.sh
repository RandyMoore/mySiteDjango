#!/usr/bin/env bash

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
        echo "Postgres never came up!"
        exit 1
    fi

    sleep 2
done