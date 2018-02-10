#!/usr/bin/env sh
# Run this to bring up a local docker postgres for use with manage.py runserver
# To run postgres and include data in imagae (you can do a do
# docker run -p 5432:5432 -e PGDATA=/var/lib/postgresql/pgdata postgres
# ./manage.py migrate
# ./upload_audit_docs.py <paths of .json files>
# docker commit -c "ENV PGDATA /var/lib/postgresql/pgdata" <container id> postgrespopulated
# Or you can run the base postgres image, populate as above, dump contents to a SQL file, then quickly reload elsewhere.
# pg_dump -U postgres postgresql://0.0.0.0  > dump.sql
# Reload locally:
#   psql -U postgres postgresql://0.0.0.0 < dump.sql
# Reload to instance within a container that doesn't have db port exposed as below
#   cat dump.sql | docker exec -i <postgres container id>  psql -U postgres postgresql://0.0.0.0
# Dump from a container that doesn't have db port exposed as below
#   docker exec -i <postgres container id>  pg_dump -U postgres postgresql://0.0.0.0 > dump.sql
docker run -p 5432:5432 postgres