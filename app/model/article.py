# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.model.article
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""

from app.model import db


class Article(db.Model):

    __tablename__ = "articles"

    id = db.Column(db.Integer(), primary_key=1)

    title = db.Column(db.String(), unique=1, nullable=0)

    cover = db.Column(db.String(), unique=0, nullable=0)

    digest = db.Column(db.String(), unique=1, nullable=0)

    content = db.Column(db.String(), unique=1, nullable=0)

    account_id = db.Column(db.Integer(), db.ForeignKey("accounts.id"))

    def __init__(self, title="", cover="", digest="", content="", account=None):

        self.title = title

        self.cover = cover

        self.digest = digest

        self.content = content

        self.account = account

    def __repr__(self):

        return self.title

    def to_json(self):

        article = dict()

        article["id"] = self.id

        article["title"] = self.title

        article["cover"] = self.cover

        article["digest"] = self.digest

        article["content"] = self.content

        article["account"] = self.account

        return article
