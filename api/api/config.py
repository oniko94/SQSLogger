# -*- coding: utf-8 -*-
import base64
import logging
import os
import sys
from typing import get_type_hints


class ConfigBaseError(Exception):
    pass


class ConfigFieldMissingError(ConfigBaseError):
    """
    Exception raised when a required variable is missing in the environment

    Parameter
    ---------
    field : str
        A variable required by the configuration manager
    """
    def __init__(self, field, message=""):
        self.message = f"{field} is required, but is missing"
        super().__init__(self.message)


class ConfigTypeCastingError(ConfigBaseError):
    """
    Exception raised when attempting to cast type of a value to a required by config fails

    Parameters
    ----------
    value : Any
        A value used in the type conversion

    field : str
        A config object field

    f_type : Any
        The type attempted to cast to
    """
    def __init__(self, value, field, f_type, message=""):
        self.message = f"Cannot cast value of {env[field]} to type of {f_type} for {field}"
        super().__init__(self.message)


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

            self.__setattr__(field, self.__get_env_var(field, env))

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

    def __get_env_var(self, field: str, env: os.environ) -> any:
        try:
            default_value = getattr(self, field, None)
        except Exception as e:
            raise ConfigBaseError(e)
        else: 
            if default_value is None and env.get(field) is None:
                raise ConfigFieldMissingError(field)

        # Cast the values to correct types
        f_type = get_type_hints(ConfigManager)[field]

        try:
            value = f_type(env.get(field, default_value))
        except ValueError:
            raise ConfigTypeCastingError(value, field, f_type)
        else:
            return value


logger = logging.getLogger("uvicorn.error")

try:
    config = ConfigManager(os.environ)
except ConfigBaseError as e:
    logger.error(e)
    sys.exit(1)
