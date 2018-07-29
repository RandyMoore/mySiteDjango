FROM baseimage
# required, no default here for security
ARG django_secret_key

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y nginx postgresql-client libpq-dev python3-pip zlib1g-dev libjpeg-dev

ADD config/requirements.txt /usr/local/etc/

RUN pip3 install -r /usr/local/etc/requirements.txt

# Everything here on doesn't require downloads - can be changed with quick image rebuild times
COPY config/* /usr/local/etc/
COPY my_site_django /usr/local/src/

RUN /bin/sh /usr/local/etc/setup.sh

EXPOSE 80

ENV DJANGO_SECRET_KEY $django_secret_key
ENV DJANGO_SETTINGS_MODULE "my_site_django.prod_settings"

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
