
from phenopy.sql.postgres import DAO
from phenopy.sql.common import *

class AccountDAO(DAO):

    class metadata(object):
        __table__ = 'account'
        id = column(primary_key=True)
        login = column()
        passwd_hash = column()
        passwd_salt = column()


