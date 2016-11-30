# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.instance.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""

import os


SECRET_KEY = "MPWeChatRSS"

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(), "db.sqlite")

with open("user_agents.txt", 'r') as temp:

    USER_AGENTS = temp.read().splitlines()