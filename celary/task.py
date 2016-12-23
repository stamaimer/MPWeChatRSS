# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.celery.task
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 12/07/16

"""

from app.model.account import Account
from app.api import gen_feed

from celary import celery

import requests


@celery.task
def poll():

    payload = dict(title=u"抓取通知")

    try:

        accounts = Account.query.all()

        for account in accounts:

            gen_feed(account)

    except Exception as e:

        payload["desp"] = e.message

