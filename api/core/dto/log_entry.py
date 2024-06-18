# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel

from core.database.models import LogEntry


class BaseDTO(BaseModel):
    """
    A Pydantic model we use to correctly map the only fields we need from the incoming request.

    It's better not to allow fields like id/pk and timestamp to be overridden with data from request body.

    Attributes
    ----------
    message : str
        The log entry message

    level : str
        The log entry level of severity/importance (i.e. debug, info etc.)
    """

    message: str
    level: str


class ModelDTO(BaseDTO):
    """
    A Pydantic model we use to display the data to the user, includes the fields left out in the base model.

    We assume that where this model is used, no data will be written but displayed.

    Attributes
    ----------
    message : str
        (Inherited from api.api.schemas.LogEntryBase) The log entry message

    level : str
        (Inherited from api.api.schemas.LogEntryBase) The log entry level of severity/importance (i.e. debug, info etc.)

    pk : int
        ID (primary key) of an entry in the database; Used for indexing

    timestamp : datetime.datetime
        An exact timestamp of the log
    """

    pk: int
    timestamp: datetime


# Explicit mapping is more Pythonic
# Also grants more control over data
def map_dto(db_entry: LogEntry) -> ModelDTO:
    """
    A function used to map the SQLAlchemy ORM fields to Pydantic model ones.

    Parameter
    ---------
    db_entry : api.api.models.LogEntry
        A SQLAlchemy model representation we store in the DB

    Returns
    -------
    api.api.schemas.LogEntry
        A Pydantic representation of the LogEntry data from the DB
    """
    return ModelDTO(
        pk=db_entry.pk,
        message=db_entry.message,
        level=db_entry.level,
        timestamp=db_entry.timestamp,
    )
