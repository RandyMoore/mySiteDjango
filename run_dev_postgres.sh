#!/usr/bin/env sh
# image is based on postgres base image, populated with manage.py migrate and other data. e.g.
# docker run -p 5432:5432 -e PGDATA=/var/lib/postgresql/pgdata postgres
# ./manage.py migrate
# ./upload_audit_docs.py <paths of .json files>
# docker commit -c "ENV PGDATA /var/lib/postgresql/pgdata" <container id> postgrespopulated
docker run -p 5432:5432 -e PGDATA=/var/lib/postgresql/pgdata postgrespopulated:ne5
