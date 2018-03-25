# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.api
    ~~~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""


import time
import inspect
import traceback

import requests
import requests_cache

from lxml import html
from fake_useragent import UserAgent

from flask import current_app, Blueprint, jsonify


ua = UserAgent()

api = Blueprint("api", __name__)

requests_cache.install_cache(expire_after=3)


@api.errorhandler(404)
def not_found(e):

    return jsonify(None), 404


def bind_ip():

    try:

        response = requests.get(current_app.config["BIND_URL"])

        current_app.logger.info(u"绑定机器IP: " + response.text)

    except:

        current_app.logger.error(traceback.format_exc())


def get_proxies():

    try:

        proxies = dict()

        response = requests.get(current_app.config["PROXY_URL"])

        current_app.logger.info(u"获取代理IP:  " + response.text)

        if response.ok and (':' in response.text):

            proxies["http"] = "http://" + response.text

        else:

            requests_cache.clear()

    except:

        current_app.logger.error(traceback.format_exc())

        requests_cache.clear()

    finally:

        return proxies