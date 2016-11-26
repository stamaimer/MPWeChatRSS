# -*- coding: utf-8 -*-

"""
    MPWeChatRSS.app.main
    ~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/14/16

"""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.api import get_account

from app.form import MPWeChatForm

from app.model import db
from app.model.account import Account
from app.model.article import Article


main = Blueprint("main", __name__)


@main.route('/', methods=["GET"])
def index():

    mp_wechat_form = MPWeChatForm()

    return render_template("index.html", mp_wechat_form=mp_wechat_form)


@main.route('/', methods=["POST"])
def insert_mp_wechat():

    mp_wechat_form = MPWeChatForm(request.form)

    if mp_wechat_form.validate():

        query = mp_wechat_form.query.data

        account = Account.query.filter((Account.name == query) | (Account.text == query)).first()

        if not account:

            new_account = get_account(query)

            db.session.add(new_account)

            db.session.commit()

            flash(query + u"已添加")

        else:

            flash(query + u"已存在")

    else:

        flash(u"出错啦！")

    # return rss url

    return redirect(url_for("main.index"))
