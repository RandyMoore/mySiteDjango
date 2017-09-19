FROM phusion/baseimage
# required, no default here for security
ARG django_secret_key

RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3.6 python3.6-dev build-essential postgresql-client wget

# Only add in requirements.txt for now, so temp docker image can be cached in case other files in config/ are edited
ADD config/requirements.txt /usr/local/etc/

RUN cd /tmp && wget https://bootstrap.pypa.io/get-pip.py && \
python3.6 get-pip.py && ln -s /usr/bin/python3.6 /usr/local/bin/python3 && \
pip3 install --upgrade pip && pip3 install -r /usr/local/etc/requirements.txt

# Everything here on doesn't require downloads - can be changed with quick image rebuild times
ADD config/* /usr/local/etc/

ADD my_site_django /usr/local/src/

RUN /bin/sh /usr/local/etc/setup.sh

EXPOSE 80

ENV DJANGO_SECRET_KEY $django_secret_key
ENV DJANGO_SETTINGS_MODULE "my_site_django.prod_settings"

# Clean up APT when done.
RUN apt-get purge -y build-essential python3.6-dev wget && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


