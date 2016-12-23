# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.model.user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 12/22/16

"""

from flask_security import UserMixin
from app.model import db, roles_users


class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=1)

    email = db.Column(db.String(255), unique=1)

    active = db.Column(db.Boolean())

    password = db.Column(db.String(255))

    # confirmed_at = db.Column(db.DateTime())

    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))

    def __init__(self, email="", active=1, password="", roles=None):

        self.roles = roles

        self.email = email

        self.active = active

        self.password = password

    def __repr__(self):

        return self.email

    def to_json(self):

        user = dict()

        user["id"] = self.id

        user["roles"] = self.roles

        user["email"] = self.email

        user["active"] = self.active

        return user


