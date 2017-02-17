# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.celery.task
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 12/07/16

"""


from app.model.account import Account
from app.model.article import Article
from app.api import bind_ip, gen_feed

from celary import celery

import traceback
import requests
import logging

from instance.config import INFORM_URL


@celery.task
def poll():

    payload = dict(text="MPWeChatRSS", desp="Finished")

    accounts = Account.query.all()

    bind_ip()

    for account in accounts:

        try:

            gen_feed(account)

        except Exception as e:

            traceback.print_exc()

            payload["desp"] += "\n\n\n\n" + account.name + "\n\n" + traceback.format_exc() + "\n\n"

            continue

    article_counts = Article.query.count()

    payload["desp"] += "\n\n" + "aritcle counts: " + str(article_counts)

    response = requests.post(INFORM_URL, data=payload)

    logging.info(str(response.status_code) + "\t" + response.reason)
