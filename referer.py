# -*- coding: utf-8 -*-

"""

    WeChatCrawler.referer
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 11/24/16

"""

import requests
from flask import Flask, request, send_file


app = Flask(__name__)


@app.route('/', methods=["GET"])
def referer():

    url = request.args.get("url", "")

    if url:

        headers = dict()

        headers["Referer"] = "http://weixin.sogou.com/"

        headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"

        response = requests.get("http://img02.store.sogou.com/net/a/05/link?appid=100520091&url=" + url, headers=headers, stream=1)

        return send_file(response.raw)

    else:

        return ""


if __name__ == "__main__":

    app.run()
