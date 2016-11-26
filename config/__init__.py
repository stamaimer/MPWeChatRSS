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

    SQLALCHEMY_ECHO = 1

    SQLALCHEMY_TRACK_MODIFICATIONS = 1


from development import DevelopmentConfig
from production import ProductionConfig
from staging import StagingConfig
