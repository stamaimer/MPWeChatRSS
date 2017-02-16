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

    title = db.Column(db.String(255), unique=1)

    cover = db.Column(db.String(255))

    digest = db.Column(db.String(255))

    content = db.Column(db.Text())

    read_num = db.Column(db.Integer())

    post_date = db.Column(db.Date())

    account_id = db.Column(db.Integer(), db.ForeignKey("accounts.id"))

    def __init__(self, title="", cover="", digest="", content="", read_num=0, post_date="", account=None):

        self.title = title

        self.cover = cover

        self.digest = digest

        self.content = content

        self.account = account

        self.read_num = read_num

        self.post_date = post_date

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

        article["read_num"] = self.read_num

        article["post_date"] = self.post_date

        return article
