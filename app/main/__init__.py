# -*- coding: utf-8 -*-

"""
    MPWeChatRSS.app.main
    ~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/14/16

"""

import requests
import requests_cache

from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for

from app.api import get_account, gen_feed, retrieve

from app.form import MPWeChatForm
from app.model.account import Account


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

            account = get_account(query)

            feed = gen_feed(account)

            flash(query + u"已添加！订阅地址：" + feed.url)

        else:

            feed_url = account.feed.url

            flash(query + u"已存在！订阅地址：" + feed_url)

    else:

        flash(u"出错啦！")

    return redirect(url_for("main.index"))


@main.route("/a2link")
def a2link():

    url = request.args.get("url", "")

    if url:

        headers = dict()

        headers["referer"] = "http://weixin.sogou.com"

        response = retrieve(url, headers)

        return send_file(response.raw)

    else:

        return None

