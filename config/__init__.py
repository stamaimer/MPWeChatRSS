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

    SECRET_KEY = "MPWeChatRSS"


from development import DevelopmentConfig
from production import ProductionConfig
from staging import StagingConfig
