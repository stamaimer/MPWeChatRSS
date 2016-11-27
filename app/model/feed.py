# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.model.feed
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/27/16

"""

from app.model import db


class Feed(db.Model):

    __tablename__ = "feeds"

    id = db.Column(db.Integer(), primary_key=1)

    url = db.Column(db.String(), unique=1, nullable=0)

    account_id = db.Column(db.Integer(), db.ForeignKey("accounts.id"))

    def __init__(self, url="", account=None):

        self.url = url

        self.account = account

    def __repr__(self):

        return self.account.text + u"的订阅地址"

    def to_json(self):

        feed = dict()

        feed["id"] = self.id

        feed["url"] = self.url

        feed["account"] = self.account

        return feed
