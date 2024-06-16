# -*- coding: utf-8 -*-
import logging
import os
import sys
from typing import get_type_hints


class ConfigError(Exception):
    pass


class ConfigManager:
    """ 
    An object for centralized storage of configurational variables.

    Retrieves values of environment variables. Is initialized once per runtime. 
    Intended to act as a single source of truth when imported elsewhere in the code.
    """
    AWS_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    AWS_SECRET_KEY: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    SQS_QUEUE_URL: str

    def __init__(self, env: os.environ):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            default_value = getattr(self, field, None)

            if default_value is None and env.get(field) is None:
                raise ConfigError(f"The {field} field is required.")

            # Cast the values to correct types
            f_type = get_type_hints(ConfigManager)[field]
            value = f_type(env.get(field, default_value))

            try:
                self.__setattr__(field, value)
            except ValueError:
                raise ConfigError(f"Cannot cast value of {env[field]} to type of {f_type} for {field}")

        # Build the database URL from env vars and store it in the config object
        db_url = "postgresql+asyncpg://{user}:{pwd}@/{db}?host={host}:{port}".format(
            user=self.POSTGRES_USER,
            pwd=self.POSTGRES_PASSWORD,
            db=self.POSTGRES_DB,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT
        )
        self.__setattr__("DB_URL", db_url)

    def __repr__(self):
        return str(self.__dict__)


logger = logging.getLogger("uvicorn.error")

try:
    config = ConfigManager(os.environ)
except ConfigError as e:
    logger.error(e)
    sys.exit(1)
