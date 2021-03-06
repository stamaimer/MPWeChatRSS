# -*- coding: utf-8 -*-

"""
    MPWeChatRSS.app.main
    ~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/14/16

"""


import os
import traceback

from urlparse import urlparse, parse_qs

from flask import Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, url_for

from app.api import get_account, gen_feed, retrieve

from app.form import MPWeChatForm

from app.model.feed import Feed
from app.model.account import Account

from app.utilities import cache


main = Blueprint("main", __name__)


def cache_key():

    return request.url


@main.route('/', methods=["GET"])
def index():

    mp_wechat_form = MPWeChatForm()

    feeds = Feed.query.all()

    return render_template("index.html", mp_wechat_form=mp_wechat_form, feeds=feeds)


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
@cache.cached(key_prefix=cache_key)
def a2link():

    try:

        url = request.args.get("url")

        current_app.logger.debug(url)

        if url:

            image_type = parse_qs(urlparse(url).query).get("wx_fmt", [""])[0]

            magic_link = "http://img02.store.sogou.com/net/a/05/link?appid=100520091&url="

            response = retrieve(magic_link + url, dict(referer="http://weixin.sogou.com"))

            return response.content, {"content-type": "image/" + image_type}

        else:

            current_app.logger.info("Empty Image URL")

            return "", 204

    except:

        current_app.logger.info(traceback.format_exc())

        return '', 204


@main.route("/feed/<name>")
def feed(name):

    return send_from_directory(os.getcwd() + "/app/static/feeds", name + ".xml")
