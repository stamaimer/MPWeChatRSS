# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.model.account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""


from app.model import db


class Account(db.Model):

    __tablename__ = "accounts"

    id = db.Column(db.Integer(), primary_key=1)

    name = db.Column(db.String(255), unique=1, nullable=0)

    text = db.Column(db.String(255), unique=1, nullable=0)

    info = db.Column(db.String(255), unique=0, nullable=1)

    auth = db.Column(db.String(255), unique=0, nullable=1)

    feed = db.relationship("Feed", cascade="all,delete", backref="account", uselist=0)

    articles = db.relationship("Article", cascade="all,delete", backref="account", lazy="dynamic")

    def __init__(self, name="", text="", info="", auth=""):

        self.name = name

        self.text = text

        self.info = info

        self.auth = auth

    def __repr__(self):

        return self.text

    def to_json(self):

        account = dict()

        account["id"] = self.id

        account["name"] = self.name

        account["text"] = self.text

        account["info"] = self.info

        account["auth"] = self.auth

        return account
