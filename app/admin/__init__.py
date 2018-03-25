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
from flask_admin.contrib.sqla.view import func

from app.model import db
from app.model.role import Role
from app.model.user import User
from app.model.feed import Feed
from app.model.account import Account
from app.model.article import Article


class AppModelView(ModelView):

    def is_accessible(self):

        return current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for("security.login", next=request.url))


class AccountModelView(AppModelView):

    column_list = ["name", "text", "article_count"]

    def get_query(self):

        return self.session.query(Account.id, Account.name, Account.text,
                                  func.count(Article.id).label("article_count")).join(Article).group_by(Account.id)

    def get_count_query(self):

        return self.session.query(func.count('*'))


class ArticleModelView(AppModelView):

    can_edit = 0

    can_create = 0

    can_view_details = 1

    column_exclude_list = ["cover", "content"]


admin = Admin(name="MPWeChat Dashboard", template_mode="bootstrap3")

admin.add_view(AppModelView(Role, db.session))
admin.add_view(AppModelView(User, db.session))
admin.add_view(AppModelView(Feed, db.session))
admin.add_view(AccountModelView(Account, db.session))
admin.add_view(ArticleModelView(Article, db.session))
