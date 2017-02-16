# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.api
    ~~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""


import os
import re
import json
import time
import inspect
import traceback

from datetime import datetime

import requests
import requests_cache

from lxml import html
from urllib import unquote
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
from sqlalchemy.exc import IntegrityError
from werkzeug.contrib.atom import AtomFeed, FeedEntry

from flask import current_app, url_for

from app.model import db
from app.model.feed import Feed
from app.model.account import Account
from app.model.article import Article


requests_cache.install_cache(expire_after=5)

BIND_URL = ""

HOST = "http://mp.weixin.qq.com"

SEARCH_URL = "http://weixin.sogou.com/weixin?type=1&query={}"

ACCOUNT_BASE_XPATH = "//*[@id=\"sogou_vr_11002301_box_0\"]"

ACCOUNT_TEXT_XPATH = ACCOUNT_BASE_XPATH + "//p/a/text()"

ACCOUNT_NAME_XPATH = ACCOUNT_BASE_XPATH + "//label/text()"

ACCOUNT_INFO_XPATH = ACCOUNT_BASE_XPATH + "//dl[1]/dd/text()"

ACCOUNT_AUTH_XPATH = ACCOUNT_BASE_XPATH + "//dl[2]/dd/text()"


def bind_ip():

    response = requests.get(BIND_URL)

    current_app.logger.info("Bind Status: " + response.content.upper())


def get_proxies():

    url = ""

    try:

        response = requests.get(url)

        current_app.logger.info(str(response.status_code) + "\t" + response.text)

        if response.ok and ":" in response.text:

            proxies = dict(http="http://" + response.text)

        else:

            requests_cache.clear()

            proxies = dict()

    except:

        requests_cache.clear()

        current_app.logger.info(traceback.format_exc())

    finally:

        return proxies


def retrieve(url, headers=None):

    current_app.logger.info(inspect.stack()[1][3] + " retrieve " + url)

    if not headers:

        headers = dict()

    while 1:

        headers["user-agent"] = UserAgent().random

        try:

            response = requests.get(url, headers=headers, proxies=get_proxies(), timeout=3)

            current_app.logger.info(str(response.status_code) + "\t" + response.reason)

            if response.ok and (url == response.request.url):

                if "referer" in headers:

                    return response

                return response.text

            else:

                current_app.logger.info(response.request.url)

                requests_cache.clear()

                time.sleep(3)

                continue

        except:

            current_app.logger.info(traceback.format_exc())

            requests_cache.clear()

            time.sleep(3)

            continue


def extract_elements(source, xpath):

    try:

        temp = [None]

        tree = html.fromstring(source)

        temp = tree.xpath(xpath, smart_strings=0)

    except:

        current_app.logger.info(traceback.format_exc())

    finally:

        return temp


def extract_element(source, xpath):

    return extract_elements(source, xpath)[0]


def get_account(query):

    source = retrieve(SEARCH_URL.format(query.encode("utf-8")))

    source = source.replace("<em>", '').replace("</em>", '').replace("<!--red_beg-->", '').replace("<!--red_end-->", '')

    name = extract_element(source, ACCOUNT_NAME_XPATH)

    text = extract_element(source, ACCOUNT_TEXT_XPATH)

    info = extract_element(source, ACCOUNT_INFO_XPATH)

    auth = extract_element(source, ACCOUNT_AUTH_XPATH)

    current_app.logger.debug("{name} {text} {info} {auth}".format(name=name.encode("utf-8"),
                                                                  text=text.encode("utf-8"),
                                                                  info=info.encode("utf-8"),
                                                                  auth=auth.encode("utf-8")))

    if isinstance(info, list):

        info = ""

    if isinstance(auth, list):

        auth = ""

    account = Account(name, text, info, auth)

    db.session.add(account)

    db.session.commit()

    return account


def get_content(item):

    url = HOST + item["content_url"].replace("&amp;", '&')

    source = retrieve(url)

    content = pq(source.replace("data-src", "src"))

    for image in content.items("img"):

        if image.attr.src:

            image.attr.src = unquote(url_for("main.a2link", url=image.attr.src.replace("/0?", "/640?"), _external=0))

    for selector in [".rich_media_area_extra", "#js_sponsor_ad_area", "#js_toobar3", "#js_sg_bar", "#sg_tj"]:

        content(selector).text("")

    url = url.replace("/s?", "/mp/getcomment?")

    read_num = json.loads(retrieve(url))["read_num"]

    return re.sub(r"(<iframe .*?/>)", r"\1</iframe>", content("#js_content").html()), \
           read_num, \
           content("#post-date").html()


def get_articles(url):

    source = ""

    while 1:

        source = retrieve(url)

        try:

            source = re.search("msgList = (.*);", source).group(1)

        except AttributeError:

            current_app.logger.critical(u"请输入验证码")

            time.sleep(3)

            requests_cache.clear()

            continue

        break

    for item in json.loads(source)["list"]:

        item = item["app_msg_ext_info"]

        if item["content_url"]:

            item["content"], item["read_num"], item["post_date"] = get_content(item)

        yield item


def gen_feed(account):

    source = retrieve(SEARCH_URL.format(account.name))

    url = extract_element(source, ACCOUNT_BASE_XPATH + "//p/a/@href")

    current_app.logger.info(inspect.stack()[0][3] + "\t\t\t\t" + url)

    while not url:

        requests_cache.clear()

        source = retrieve(SEARCH_URL.format(account.name))

        url = extract_element(source, ACCOUNT_BASE_XPATH + "//p/a/@href")

        current_app.logger.info(inspect.stack()[0][3] + "\t\t\t\t" + url)

    atom = AtomFeed(account.text, feed_url=url_for("main.feed", name=account.name, _external=1), author=account.auth)

    articles = get_articles(url)

    for item in articles:

        article = Article(item["title"].replace("&quot;", '"'), url_for("main.a2link", url=item["cover"], _external=1),
                          item["digest"].replace("&quot;", '"'), item["content"].replace("&quot;", '"'),
                          item["read_num"], item["post_date"], account)

        atom.add(FeedEntry(article.title, article.content, url=article.cover, updated=datetime.now()))

        try:

            db.session.merge(article)

            db.session.commit()

        except IntegrityError:

            db.session.rollback()

    with open(os.getcwd() + "/app/static/feeds/" + account.name + ".xml", 'w') as temp:

        temp.write(atom.to_string().encode("utf-8"))

    feed = Feed(atom.feed_url, account)

    try:

        db.session.merge(feed)

        db.session.commit()

    except IntegrityError:

        db.session.rollback()

    return feed
