from __future__ import with_statement
import unittest
import sys, os, inspect

from phenopy.misc import add_relative_module_path, get_abs_module_path
from phenopy.sql.common import *
from phenopy.sql.postgres import transaction
from phenopy.sql.common import *

from connection_factory import connect

from mockup_login import *


class TestAccountGenerator(unittest.TestCase):
    
    def setUp(self):
        add_relative_module_path(self.__class__, '../src')

    def cleanup_dir(self, path):
        for f in (os.path.abspath( os.path.join(path, x) ) for x in os.listdir(path) if x != '__init__.py'):
            os.remove(f)

    def test_gen_dao(self):
        from account_generator import Account_Postgres_MD5_Salt_Generator
        path = os.path.join(get_abs_module_path(self.__class__), 'account')
        self.cleanup_dir(path)
        gen = Account_Postgres_MD5_Salt_Generator(path,'Account')
        gen.generate_files()
        m = __import__('account.account_dao', fromlist=['account_dao'])
        self.assert_( m.AccountDAO(None).__class__.__name__ == 'AccountDAO')


    def test_db(self):
        from connection_factory import connect
        from account_generator import Account_Postgres_MD5_Salt_Generator
        path = os.path.join(get_abs_module_path(self.__class__), 'account')
        self.cleanup_dir(path)
        gen = Account_Postgres_MD5_Salt_Generator(path,'Account','connection_factory')
        gen.generate_files()
        with connect() as conn:
            with transaction(conn):
                cur = conn.cursor()
                try:
                    cur.execute('''DROP TABLE account CASCADE''')
                except:
                    pass

            with transaction(conn):
                cur = conn.cursor()
                try:
                    cur.execute('''DROP SEQUENCE account_pk_seq''')
                except:
                    pass

            with transaction(conn):
                cur = conn.cursor()
                sql = open( os.path.join(get_abs_module_path(self.__class__), 'account/account.sql'), 'r'  ).read()
                cur.execute(sql)

            m = __import__('account.account_biz', fromlist=['account_biz'])
            acc = m.AccountBiz()
            (passw, phash, salt) = acc.gen_password()
            idn = acc.create('test_user1', phash, salt)

            from session_storage_memcached import SessionStorageMemcached
            from login_biz import Login_Biz

            storage = SessionStorageMemcached('127.0.0.1:11211', 'test_session_storage_memcached')

            lb = Login_Biz(acc, storage)

            lb.login('test_user1', passw)


if __name__ == '__main__':
    unittest.main()

