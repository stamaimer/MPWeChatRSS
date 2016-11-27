# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.admin
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/27/16

"""

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.model import db
from app.model.feed import Feed
from app.model.account import Account
from app.model.article import Article


admin = Admin(name="MPWeChat Dashboard", template_mode="bootstrap3")

admin.add_view(ModelView(Feed, db.session))
admin.add_view(ModelView(Account, db.session))
admin.add_view(ModelView(Article, db.session))
