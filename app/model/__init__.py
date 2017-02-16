# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.model
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""


from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer(), db.ForeignKey("role.id")))


