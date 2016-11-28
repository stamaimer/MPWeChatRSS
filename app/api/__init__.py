# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.api
    ~~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""

import os
import re
import json
import requests
import requests_cache

from lxml import html
from urllib import unquote
from selenium import webdriver
from pyquery import PyQuery as pq

from flask import url_for

from app.model import db
from app.model.feed import Feed
from app.model.account import Account
from app.model.article import Article


requests_cache.install_cache(expire_after=3600)

HOST = "http://mp.weixin.qq.com"

# BROWSER = webdriver.Firefox()

SEARCH_URL = "http://weixin.sogou.com/weixin?type=1&query={}"

ACCOUNT_BASE_XPATH = "//*[@id=\"sogou_vr_11002301_box_0\"]"

ACCOUNT_TEXT_XPATH = ACCOUNT_BASE_XPATH + "//p/a/text()"

ACCOUNT_NAME_XPATH = ACCOUNT_BASE_XPATH + "//label/text()"

ACCOUNT_INFO_XPATH = ACCOUNT_BASE_XPATH + "//dl[1]/dd/text()"

ACCOUNT_AUTH_XPATH = ACCOUNT_BASE_XPATH + "//dl[2]/dd/text()"


def retrieve(url, headers=None):

    if not headers:

        headers = dict()

    headers["user-agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"

    response = requests.get(url, headers=headers)

    if "referer" in headers:

        return response

    string = response.text

    with open("test.html", "w") as temp:

        temp.write(string.encode("utf-8"))

    return string


def extract_element(string, xpath):

    tree = html.fromstring(string)

    temp = tree.xpath(xpath, smart_strings=0)

    if 1 == len(temp):

        return temp[0]

    else:

        return temp


def get_account(query):

    string = retrieve(SEARCH_URL.format(query.encode("utf-8")))

    string = string.replace("<em>", '').replace("</em>", '')

    name = extract_element(string, ACCOUNT_NAME_XPATH)

    text = extract_element(string, ACCOUNT_TEXT_XPATH)

    info = extract_element(string, ACCOUNT_INFO_XPATH)

    auth = extract_element(string, ACCOUNT_AUTH_XPATH)

    print name, text, info, auth

    if isinstance(auth, list):

        auth = ""

    account = Account(name, text, info, auth)

    db.session.add(account)

    return account


def get_articles(url):

    string = retrieve(url)

    source = re.search("msgList = (.*);", string).group(1)

    for item in json.loads(source)["list"]:

        item = item["app_msg_ext_info"]

        url = HOST + item["content_url"].replace("&amp;", '&')

        string = retrieve(url)

        with open(os.getcwd() + "/app/static/articles/" + item["title"] + ".html", 'w') as temp:

            content = pq(string.replace("data-src", "src"))

            for image in content.items("img"):

                if image.attr.src:

                    image.attr.src = unquote(url_for("main.a2link", url=image.attr.src, _external=1))

            temp.write(content.html().encode("utf-8"))


def gen_feed(account):

    string = retrieve(SEARCH_URL.format(account.name))

    url = extract_element(string, ACCOUNT_BASE_XPATH + "//p/a/@href")

    # print url

    articles = get_articles(url)

    feed = Feed(url, account)

    db.session.add(feed)

    return feed
