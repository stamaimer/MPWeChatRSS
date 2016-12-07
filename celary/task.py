# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.celery.tasks
    ~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 12/07/16

"""

from app.model.account import Account
from app.api import gen_feed

from celary import celery


@celery.task
def poll():

    accounts = Account.query.all()

    for account in accounts:

        gen_feed(account)
