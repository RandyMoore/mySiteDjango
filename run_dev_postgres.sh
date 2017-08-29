#!/usr/bin/env sh
docker run -p 5432:5432 -v postgres-data:/var/lib/postgresql/data postgres
