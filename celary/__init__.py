# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.celery
    ~~~~~~~~~~~~~~~~~~

    stamaimer 11/29/16

"""

from app import create_app
from celery import Celery


def create_celery(app):

    celery = Celery(app.import_name, broker="amqp://guest:guest@localhost:5672//", backend="rpc://", include=["celary.task"])

    celery.config_from_object("config")

    TaskBase = celery.Task

    class ContextTask(TaskBase):

        abstract = 1

        def __call__(self, *args, **kwargs):

            with app.app_context():

                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

celery = create_celery(create_app("config.DevelopmentConfig"))

if __name__ == '__main__':

    celery.start()
