# -*- coding: utf-8 -*-
import os

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
# Can be None
AWS_ENDPOINT = os.environ.get("AWS_ENDPOINT_URL")
AWS_REGION = os.environ["AWS_REGION"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
# Port is not really significant, assume default
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_USER = os.environ["POSTGRES_USER"]
DB_URL = (
    "postgresql+asyncpg://{user}:{pwd}@/{db}?host={host}:{port}".format(
        user=POSTGRES_USER,
        pwd=POSTGRES_PASSWORD,
        db=POSTGRES_DB,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
)
SQS_QUEUE_NAME = os.environ["SQS_QUEUE_NAME"]
