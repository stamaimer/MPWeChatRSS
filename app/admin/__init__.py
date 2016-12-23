# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.admin
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/27/16

"""

from flask import redirect, request, url_for

from flask_security import current_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.model import db
from app.model.role import Role
from app.model.user import User
from app.model.feed import Feed
from app.model.account import Account
from app.model.article import Article


class AppModelView(ModelView):

    pass

    # def is_accessible(self):
    #
    #     return current_user.has_role("admin")
    #
    # def inaccessible_callback(self, name, **kwargs):
    #
    #     return redirect(url_for("security.login", next=request.url))

admin = Admin(name="MPWeChat Dashboard", template_mode="bootstrap3")

admin.add_view(AppModelView(Role, db.session))
admin.add_view(AppModelView(User, db.session))
admin.add_view(AppModelView(Feed, db.session))
admin.add_view(AppModelView(Account, db.session))
admin.add_view(AppModelView(Article, db.session))
