# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.api
    ~~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""

import requests
import requests_cache

from lxml import html

from app.model.account import Account


requests_cache.install_cache()

SEARCH_URL = "http://weixin.sogou.com/weixin?type=1&query={}"

ACCOUNT_BASE_XPATH = "//*[@id=\"sogou_vr_11002301_box_0\"]"

ACCOUNT_TEXT_XPATH = ACCOUNT_BASE_XPATH + "//em/text()"

ACCOUNT_NAME_XPATH = ACCOUNT_BASE_XPATH + "//label/text()"

ACCOUNT_INFO_XPATH = ACCOUNT_BASE_XPATH + "//dl[1]/dd/text()"

ACCOUNT_AUTH_XPATH = ACCOUNT_BASE_XPATH + "//dl[2]/dd/text()"


def extract_element(string, xpath):

    tree = html.fromstring(string)

    temp = tree.xpath(xpath, smart_strings=0)

    if 1 == len(temp):

        return temp[0]

    else:

        return temp


def get_account(query):

    response = requests.get(SEARCH_URL.format(query.encode("utf-8")))

    string = response.text

    with open("test.html", "w") as file:

        file.write(string.encode("utf-8"))

    name = extract_element(string, ACCOUNT_NAME_XPATH)

    text = extract_element(string, ACCOUNT_TEXT_XPATH)

    info = extract_element(string, ACCOUNT_INFO_XPATH)

    auth = extract_element(string, ACCOUNT_AUTH_XPATH)

    print name, text, info, auth

    return Account(name, text, info, str(auth))

