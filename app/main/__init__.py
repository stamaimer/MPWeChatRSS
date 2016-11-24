# -*- coding: utf-8 -*-

"""
    MPWeChatRSS.app.main
    ~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/14/16

"""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.form import MPWeChatForm


main = Blueprint("main", __name__)


@main.route('/', methods=["GET"])
def index():

    mp_wechat_form = MPWeChatForm()

    return render_template("index.html", mp_wechat_form=mp_wechat_form)


@main.route('/', methods=["POST"])
def insert_mp_wechat():

    mp_wechat_form = MPWeChatForm(request.form)

    if mp_wechat_form.validate():

        flash(mp_wechat_form.mp_wechat.data)

    else:

        flash(u"出错啦！")

    return redirect(url_for("main.index"))


def