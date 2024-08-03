#! /bin/bash

# Start Postgres container
docker run --detach \
	--name postgres \
	--env POSTGRES_PASSWORD=password \
	--env POSTGRES_USER=postgres \
	--publish 5432:5432 \
	postgres
