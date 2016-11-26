# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.manage
    ~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.model import db


app = create_app("config.DevelopmentConfig")

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command("db", MigrateCommand)


if __name__ == "__main__":

    manager.run()