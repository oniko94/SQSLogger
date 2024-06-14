#!/bin/sh
alembic revision --autogenerate; alembic upgrade head
exec fastapi run api/main.py
