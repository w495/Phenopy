
from __future__ import with_statement
import phenopy.passwords as passwd
from phenopy.sql.common import *
from phenopy.sql.postgres import transaction

from dao.connection_factory import connect

from account_dao import AccountDAO

class AccountBiz:

    def gen_password(self, password=None, length=8, salt_length=10):
        return passwd.generate(password, length, salt_length)

    def is_password_match(self, account, password):
        return passwd.check(password, account.passwd_hash, account.passwd_salt)

    def get_account_by(self, login):
        with connect() as conn:
            dao = AccountDAO(conn)
            return dao.get(eq('login', login))

    def create(self, login, passwd_hash, passwd_salt):
        with connect() as conn:
            with transaction(conn):
                dao = AccountDAO(conn)
                return dao.create(login=login, passwd_hash=passwd_hash, passwd_salt=passwd_salt)

    def update(self, id, passwd_hash, passwd_salt):
        with connect() as conn:
            with transaction(conn):
                dao = AccountDAO(conn)
                return dao.update(eq('id',id),  passwd_hash=passwd_hash, passwd_salt=passwd_salt)

    def delete(self, id):
        with connect() as conn:
            with transaction(conn):
                dao = AccountDAO(conn)
                return dao.delete(eq('id',id))

