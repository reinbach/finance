from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

import config


class DB():
    def __init__(self):
        self.metadata = MetaData()
        #TODO start with session as None
        # and only when called set it
        self.session = self.get_session()

    def get_conn_param(self):
        if hasattr(config, 'TESTING') and config.TESTING:
            db_name = config.DATABASE.get('DB_NAME_TESTING')
        else:
            db_name = config.DATABASE.get('DB_NAME')

        conn_param = "{backend}://{user}:{db_pass}@{host}/{name}".format(
            backend=config.DATABASE.get('DB_BACKEND', 'postgresql'),
            user=config.DATABASE.get('DB_USER', ''),
            db_pass=config.DATABASE.get('DB_PASS', ''),
            host=config.DATABASE.get('DB_HOST', 'localhost'),
            name=db_name
        )
        return conn_param

    def get_engine(self):
        engine = create_engine(
            self.get_conn_param(),
            convert_unicode=True
        )
        return engine

    def get_session(self):
        """Get db session object"""
        db_session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.get_engine()
            )
        )
        return db_session

    # def drop_db(self):
    #     """Drop all tables in the models

    #     Only allow this for testing purposes
    #     """
    #     if hasattr(config, 'TESTING') and config.TESTING:
    #         from models import *  # noqa
    #         self.metadata.drop_all(bind=self.get_engine())
