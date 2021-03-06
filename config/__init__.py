# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.config
    ~~~~~~~~~~~~~~~~~~

    stamaimer 11/24/16

"""


class Config(object):

    # configuration of flask

    HOST = "127.0.0.1"

    PORT = 5000

    SERVER_NAME = "127.0.0.1:5000"

    CACHE_TYPE = "simple"

    SQLALCHEMY_ECHO = 0

    SQLALCHEMY_POOL_SIZE = 20

    SQLALCHEMY_POOL_RECYCLE = 10

    SQLALCHEMY_COMMIT_ON_TEARDOWN = 0

    SQLALCHEMY_TRACK_MODIFICATIONS = 1


from development import DevelopmentConfig
from production import ProductionConfig
from staging import StagingConfig
