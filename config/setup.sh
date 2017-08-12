#!/bin/bash -x

# Add our Nginx config
ln -s /usr/local/etc/nginx_server.conf /etc/nginx/conf.d/nginx.conf
rm /etc/nginx/nginx.conf
ln -s /usr/local/etc/nginx.conf /etc/nginx/nginx.conf
mkdir /etc/service/nginx
cp /usr/local/etc/nginx.sh /etc/service/nginx/run
chmod +x /etc/service/nginx/run
rm /etc/nginx/sites-enabled/default # So to not override our config

# Add our uWSGI config
mkdir -p /etc/uwsgi/vassals
ln -s /usr/local/etc/uwsgi.ini /etc/uwsgi/vassals/
mkdir /etc/service/uwsgi
cp /usr/local/etc/uwsgi.sh /etc/service/uwsgi/run
chmod +x /etc/service/uwsgi/run

# Add missing directories, set permissions
mkdir /var/run/www
mkdir /var/run/www/media
mkdir /var/run/www/static
chown -R www-data:www-data /var/run/www
mkdir /var/log/uwsgi
chown -R www-data:www-data /var/log/uwsgi

# Put static and media files in location for access by webserver - do this during image build
cd /usr/local/src
chmod +x manage.py
./manage.py collectstatic
if [ -d media ]; then
  cp -r media/* /var/run/www/media/
fi

# Setup scripts to execute 1 time commands on container start - this is a feature of phusion/baseimage
# https://github.com/phusion/baseimage-docker#running_startup_scripts
mkdir -p /etc/my_init.d
ln -s /usr/local/etc/startup.sh /etc/my_init.d/
chmod +x /etc/my_init.d/startup.sh