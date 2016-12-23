# -*- coding: utf-8 -*-

"""

    MPWeChatRSS.app.security
    ~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 12/22/16

"""

from flask_security import Security, SQLAlchemyUserDatastore

from app.model import db

from app.model.role import Role
from app.model.user import User

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(datastore=user_datastore)
