from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

import config

metadata = MetaData()

def get_conn_param():
    if hasattr(config, 'TESTING') and config.TESTING:
        db_name = config.DATABASE.get('DB_NAME_TESTING')
    else:
        db_name = config.DATABASE.get('DB_NAME')

    conn_param = "{db_backend}://{db_user}:{db_pass}@{db_host}/{db_name}".format(
        db_backend=config.DATABASE.get('DB_BACKEND', 'postgresql'),
        db_user=config.DATABASE.get('DB_USER', ''),
        db_pass=config.DATABASE.get('DB_PASS', ''),
        db_host=config.DATABASE.get('DB_HOST', 'localhost'),
        db_name=db_name
    )
    return conn_param

def get_engine():
    engine =  create_engine(
        get_conn_param(),
        convert_unicode=True
    )
    return engine

def get_db_session():
    """Get db session object"""
    db_session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=get_engine()
            )
        )
    return db_session

def init_db():
    # import all modules here that might define models so
    # that they will be registered properly on the metadata.
    # Otherwise you will have to import them first before
    # calling init_db()
    import models
    metadata.create_all(bind=get_engine())

def drop_db():
    """Drop all tables in the models

    Only allow this for testing purposes
    """
    if hasattr(config, 'TESTING') and config.TESTING:
        import models
        metadata.drop_all(bind=get_engine())
