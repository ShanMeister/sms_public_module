# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Engine, event
from sqlalchemy.orm import sessionmaker
from loguru import logger
import os

from shared.app.enums.app_run_mode import AppRunMode
from shared.app.library.util import load_bool_from_env

if os.getenv('APP_ENV') == AppRunMode.DEBUG.value:
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        logger.info(f"Query stat: {statement}, param: {parameters}")


class MySQLImplement:
    def __init__(self):
        try:
            connection_uri = "mysql+pymysql://{}:{}@{}:{}/{}".format(
                os.getenv('SCX_MYSQL_ACCOUNT'),
                os.getenv('SCX_MYSQL_PASSWORD'),
                os.getenv('SCX_MYSQL_HOST'),
                int(os.getenv('SCX_MYSQL_PORT')),
                os.getenv('SCX_MYSQL_DATABASE_NAME')
            )

            pre_ping = load_bool_from_env('SCX_MYSQL_POOL_PRE_PING')
            engine = create_engine(
                connection_uri,
                max_overflow=int(os.getenv('SCX_MYSQL_MAX_CONNECTION')),
                pool_recycle=int(os.getenv('SCX_MYSQL_POOL_RECYCLE')),
                pool_pre_ping=pre_ping,
            )

            self.Session = sessionmaker(bind=engine)

            logger.info("create connection pool to MySQL success")
        except Exception as e:
            logger.warning(f"connection to MySQL failed: {e}")

    def get_connection(self):
        return self.Session()


mysql_object = MySQLImplement()
