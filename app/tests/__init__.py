# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.tests
    ~~~~~~~~~~~~~~~~~

    stamaimer 11/25/16

"""

import os
import unittest
import tempfile

from app import create_app
from app.model import db


class MPWeChatRSSTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app("config.TestingConfig")

        self.db_fd, self.app.config["SQLALCHEMY_DATABASE_URI"] = tempfile.mkstemp()

        with self.app.app_context():

            db.create_all()

    def tearDown(self):

        os.close(self.db_fd)

        os.unlink(self.app.config["SQLALCHEMY_DATABASE_URI"])


if __name__ == "__main__":

    unittest.main()
