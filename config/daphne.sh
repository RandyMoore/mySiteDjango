#!/usr/bin/env sh
cd /usr/local/src
./waitForDB.sh
daphne -b 0.0.0.0 -p 8001 my_site_django.asgi:channel_layer