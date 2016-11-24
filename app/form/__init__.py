# -*- coding: utf-8 -*-

"""
    MPWeChatRSS.app.form
    ~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/24/16

"""

from wtforms import Form, StringField, validators


class MPWeChatForm(Form):

    mp_wechat = StringField(u"微信公众号：")

