# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.instance.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""

import os


SECRET_KEY = "MPWeChatRSS"

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(), "db.sqlite")

DB = "mysql"

DB_DRIVER = "pymysql"

DB_USER = ""
DB_PSWD = ""
DB_HOST = ""
DB_PORT = "3306"
DB_NAME = "mpwechatrss"

SQLALCHEMY_DATABASE_URI = "{db}+{db_driver}://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}".format(db=DB,
                                                                                                        db_driver=DB_DRIVER,
                                                                                                        db_user=DB_USER,
                                                                                                        db_pswd=DB_PSWD,
                                                                                                        db_host=DB_HOST,
                                                                                                        db_port=DB_PORT,
                                                                                                        db_name=DB_NAME)
