#!/bin/sh
uwsgi --emperor /etc/uwsgi/vassals --die-on-term --uid www-data --gid www-data --logto /var/log/uwsgi/emporer.log
