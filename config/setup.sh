#!/bin/bash -x

# Add Daphne service config
mkdir /etc/service/daphne
cp /usr/local/etc/daphne.sh /etc/service/daphne/run
chmod +x /etc/service/daphne/run

# Add Django worker config
mkdir /etc/service/worker
cp /usr/local/etc/django_worker.sh /etc/service/worker/run
chmod +x /etc/service/worker/run

# Misc
chmod +x /usr/local/src/waitForDB.sh