# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.celery.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 12/07/16

"""

from datetime import timedelta

CELERYBEAT_SCHEDULE = \
{
    'poll':
    {
        'task': 'task.poll',
        'schedule': timedelta(hours=12),
        'args': ()
    },
}

CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']