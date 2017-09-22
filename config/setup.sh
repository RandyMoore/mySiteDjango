#!/bin/bash -x

# Add our Nginx config
ln -s /usr/local/etc/nginx_server.conf /etc/nginx/conf.d/nginx.conf
rm /etc/nginx/nginx.conf
ln -s /usr/local/etc/nginx.conf /etc/nginx/nginx.conf
mkdir /etc/service/nginx
cp /usr/local/etc/nginx.sh /etc/service/nginx/run
chmod +x /etc/service/nginx/run
rm /etc/nginx/sites-enabled/default # So to not override our config

# Add Daphne service config
mkdir /etc/service/daphne
cp /usr/local/etc/daphne.sh /etc/service/daphne/run
chmod +x /etc/service/daphne/run

# Add Django worker config
mkdir /etc/service/worker
cp /usr/local/etc/django_worker.sh /etc/service/worker/run
chmod +x /etc/service/worker/run

# Set permissions
chmod +x /usr/local/src/waitForDB.sh
mkdir -p /var/run/www/media
mkdir -p /var/run/www/static
chown -R www-data:www-data /var/run/www

cd /usr/local/src
export DJANGO_SETTINGS_MODULE="my_site_django.prod_settings"
python3.6 manage.py collectstatic --noinput

if [ -d media ]; then
  cp -r media/* /var/run/www/media/
fi
