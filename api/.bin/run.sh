#!/bin/sh
# If we are running in AWS, get the platform specific variables like credentials
for env in $(printenv); do
    if [[ $env == "AWS"* ]]; then
        echo $env
    fi;
done;
# Apply migrations if necessary;
# The developer should generate and apply the migrations manually before running the application;
alembic upgrade head
exec python -m app
