#!/usr/bin/env sh
cd /usr/local/src
./waitForDB.sh
if [ -e dump.sql.bz2 ]  # For restarting container
then
    # dump contains migrations, remove those put in place by django.setup()
    dropdb -U postgres -h db -p 5432 postgres
    createdb -U postgres -h db -p 5432 postgres
    bzcat dump.sql.bz2 | psql -U postgres postgresql://db
    rm dump.sql.bz2
fi
daphne -b 0.0.0.0 -p 8001 my_site_django.asgi:application
