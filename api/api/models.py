import sys
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base


try:
    DATABASE_URL = os.environ.get("DATABASE_URL")
except KeyError:
    sys.exit("No database address found in environment; Exiting...")
finally:
    engine = create_async_engine(DATABASE_URL)

Base = declarative_base()


class LogEntry(Base):
    __tablename__ = "log_entries"
    pk = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    level = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
