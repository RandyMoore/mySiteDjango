FROM phusion/baseimage
# Use baseimage-docker's init system
CMD ["/sbin/my_init"]

ENV DOCKER=True

RUN apt-get update && apt-get upgrade -y && apt-get install -y nginx python-pip

ADD config/* /usr/local/etc/
ADD my_site_django /usr/local/src/

RUN /bin/sh /usr/local/etc/setup.sh

EXPOSE 80

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
