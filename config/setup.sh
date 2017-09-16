#!/bin/bash -x

# Add Daphne service config
mkdir /etc/service/daphne
cp /usr/local/etc/daphne.sh /etc/service/daphne/run
chmod +x /etc/service/daphne/run

# Add Django worker config
mkdir /etc/service/worker
cp /usr/local/etc/django_worker.sh /etc/service/worker/run
chmod +x /etc/service/worker/run

# Install pip for use with python 3.6 and requirements
cd /usr/local/src
wget https://bootstrap.pypa.io/get-pip.py
python3.6 get-pip.py
ln -s /usr/bin/python3.6 /usr/local/bin/python3
pip3 install --upgrade pip && pip3 install -r /usr/local/etc/requirements.txt

# Misc
chmod +x /usr/local/src/waitForDB.sh