#!/bin/bash -x

# Install Python requirements
pip install --upgrade pip
pip install -r /usr/local/etc/requirements.txt

# Add our Nginx config
ln -s /usr/local/etc/nginx.conf /etc/nginx/conf.d/ 
mkdir /etc/service/nginx
cp /usr/local/etc/nginx.sh /etc/service/nginx/run
chmod +x /etc/service/nginx/run
rm /etc/nginx/sites-enabled/default # So to not override our config

# Add our uWSGI config
mkdir /etc/uwsgi 
mkdir /etc/uwsgi/vassals 
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

# Put static and media files in location for access by webserver
cd /usr/local/src
chmod +x manage.py
./manage.py collectstatic
if [ -d media ]; then
  cp -r media/* /var/run/www/media/
fi
chown www-data:www-data db.sqlite3
mv db.sqlite3 /var/run/www/
