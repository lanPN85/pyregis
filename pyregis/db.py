from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

SQLITE_URL = 'sqlite:///' + os.path.abspath(os.getcwd() + '/data/pyregis.db')

engine = create_engine(SQLITE_URL, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Model = declarative_base()
Model.query = db_session.query_property()


def init_db():
    # noinspection PyUnresolvedReferences
    from . import models
    Model.metadata.create_all(bind=engine)


def clear_db():
    Model.metadata.drop_all(bind=engine)
    init_db()
