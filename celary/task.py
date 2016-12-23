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

INFORM_URL = "http://sc.ftqq.com/SCU436T08f5357b0dafad0249283e67c3b4e71f55f677ffe2b28.send"


@celery.task
def poll():

    payload = dict(text="MPWeChatRSS", desp="Finished")

    try:

        accounts = Account.query.all()

        for account in accounts:

            gen_feed(account)

    except Exception as e:

        payload["desp"] = e.message

    response = requests.post(INFORM_URL, data=payload)

    print response.status_code, response.reason