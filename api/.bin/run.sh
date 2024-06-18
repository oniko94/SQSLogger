#!/bin/sh
# Apply migrations if necessary;
# The developer should generate and apply the migrations manually before running the application;
alembic upgrade head
exec python -m api
