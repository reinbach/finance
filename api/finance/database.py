from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

import config

conn_param = "{db_backend}://{db_user}:{db_pass}@{db_host}/{db_name}".format(
    db_backend=config.get('DB_BACKEND', 'postgresql'),
    db_user=config.get('DB_USER', ''),
    db_pass=config.get('DB_PASS', ''),
    db_host=config.get('DB_HOST', 'localhost'),
    db_name=config.get('DB_NAME', '')
)
engine = create_engine(conn_param, convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

def init_db():
    # import all modules here that might define models so
    # that they will be registered properly on the metadata.
    # Otherwise you will have to import them first before
    # calling init_db()
    import models
    metadata.create_all(bind=engine)