#!/usr/bin/env sh
cd my_site_django
daphne my_site_django.asgi:channel_layer
