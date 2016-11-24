# -*- coding: utf-8 -*-

"""
    MPWeChatRSS.app
    ~~~~~~~~~~~~~~~

    stamaimer 11/24/16

"""

from flask import Flask


def create_app(config_name):

    app = Flask(__name__, instance_relative_config=1)

    app.config.from_object(config_name)

    app.config.from_pyfile("config.py")

    from main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
