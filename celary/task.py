# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.celery.task
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 12/07/16

"""

from app.model.account import Account
from app.api import gen_feed

from celary import celery

import traceback
import requests
import logging
import sys

INFORM_URL = ""


@celery.task
def poll():

    payload = dict(text="MPWeChatRSS", desp="Finished")

    bind_url = "http://s.zdaye.com/StApiEditIP.html?u=longhornxp1&p=KC8E4A223F5D6A09&api=201612191538359188"

    response = requests.get(bind_url)

    logging.info("Bind Status: " + response.content.upper())

    accounts = Account.query.all()

    for account in accounts:

        try:

            gen_feed(account)

        except Exception as e:

            traceback.print_exc()

            payload["desp"] += "\n\n" + account.name + "\n\n" + traceback.format_exc() + "\n\n" # e.message + str(sys.exc_info()[-1].tb_lineno)

            continue

    response = requests.post(INFORM_URL, data=payload)

    print response.status_code, response.reason