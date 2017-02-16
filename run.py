# -*- coding: utf-8 -*-

"""
    
    MPWeChatRSS.run
    ~~~~~~~~~~~~~~~

    stamaimer 11/24/16

"""


from app import create_app


app = create_app("config.DevelopmentConfig")


if __name__ == '__main__':

    app.run(host=app.config["HOST"], port=app.config["PORT"], threaded=1)

