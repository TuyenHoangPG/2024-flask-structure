import os

import sqlalchemy
from celery import Celery
from celery.signals import task_postrun
from sqlalchemy.orm import sessionmaker

from src.commons.configs.config import get_config

from .handlers.do_something_handler import do_something_handler

celery = Celery(__name__)
config = get_config(os.getenv("FLASK_ENV"))
celery.conf.update(
    broker_url=config.CELERY_BROKER_URL,
    result_backend=config.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_queues={
        f"{config.ENV}": {
            "exchange": f"tasks_{config.ENV}",
            "routing_key": f"{config.ENV}.do_some_tasks",
        }
    },
)


def connect():
    """Connects to the database and return a session"""

    uri = config.SQLALCHEMY_DATABASE_URI
    con = sqlalchemy.create_engine(uri)
    Session = sessionmaker(bind=con)
    session = Session()

    return con, session


con, session = connect()


@celery.task(
    name=f"{config.ENV}.do_some_tasks",
    queue=config.ENV,
    routing_key=f"{config.ENV}.do_some_tasks",
    exchange=f"tasks_{config.ENV}",
)
def do_something(data):
    do_something_handler(data)


@task_postrun.connect
def close_session(*args, **kwargs):
    session.close_all()
