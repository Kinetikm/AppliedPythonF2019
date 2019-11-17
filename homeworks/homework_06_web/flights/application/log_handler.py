import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.model import LogBase, Log
import datetime


class LogDBHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        engine = create_engine('sqlite:///log.db')
        LogBase.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def emit(self, record):
        dt = datetime.datetime.fromtimestamp(record.created, tz=datetime.timezone.utc)
        entry = Log(
            time=dt,
            lavel_name=record.levelname,
            name=record.name,
            remote_addr=record.remote_addr,
            method=record.method,
            scheme=record.scheme,
            full_path=record.full_path,
            json=str(record.json),
            status=record.status,
            resp_time=record.resp_time
        )
        self.session.add(entry)
        self.session.commit()
