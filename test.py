# -*- coding: utf-8 -*-

"""

    WeChatCrawler.test
    ~~~~~~~~~~~~~~~~~~

    stamaiemr 11/23/16

"""

import re
import json
import requests
import requests_cache

from lxml import html, etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from HTMLParser import HTMLParser

requests_cache.install_cache()

PARSER = HTMLParser()

# BROWSER = webdriver.Chrome()

HOST = "http://mp.weixin.qq.com"

SEARCH_URL = "http://weixin.sogou.com/weixin?type=1&query={}"

MP_WECHAT_URL_XPATH = "//*[@id=\"sogou_vr_11002301_box_0\"]/@href"

ARTICLE_CONTENT_XPATH = "//*[@id=\"js_content\"]"


def parse(source, xpath):

    tree = html.fromstring(source)

    return tree.xpath(xpath, smart_strings=0)


response = requests.get(SEARCH_URL.format("槽边往事"))

mp_wechat_url = parse(response.text, MP_WECHAT_URL_XPATH)[0]

response = requests.get(mp_wechat_url)

for item in json.loads(re.search("msgList = (.*);", response.text).group(1))["list"]:

    item = item["app_msg_ext_info"]

    article = dict()

    article["title"] = item["title"]

    article["digest"] = item["digest"]

    article["cover_url"] = item["cover"]

    article["content_url"] = HOST + PARSER.unescape(item["content_url"])

    response = requests.get(article["content_url"])

    with open(article["title"] + ".html", 'w') as file:

        content = parse(response.text, ARTICLE_CONTENT_XPATH)[0]

        content = pq(etree.tostring(content).replace("data-src", "src"))

        images = content.items("img")

        for image in images:

            image.attr.src = "http://localhost:5000?url=" + image.attr.src

            print image.attr.src

        file.write(content.outer_html().encode("utf-8"))

        print article["title"]

