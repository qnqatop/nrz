from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TriggerTable(Base):
    __tablename__ = 'change_logs'

    id = Column(Integer, primary_key=True)
    trigger_name = Column(String)
    table_name = Column(String)
    record_id = Column(Integer)
    is_synced = Column(Boolean)
    event_time = Column(DateTime)


