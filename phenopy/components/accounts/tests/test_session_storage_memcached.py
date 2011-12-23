import unittest
import sys, os, inspect

from phenopy.misc import add_relative_module_path

from mockup_login import *

class TestSessionStorageMemcached(unittest.TestCase):
    
    def setUp(self):
        add_relative_module_path(self.__class__, '../src')

    def test_one(self):
        from session_storage_memcached import SessionStorageMemcached
        from login_biz import Login_Biz
        lb = Login_Biz(Mockup_Account_Biz(), SessionStorageMemcached('127.0.0.1:11211', 'test_session_storage_memcached'))

        lb.login('test_user_1', PASSWORD)

        self.assert_( lb.is_logged_in('test_user_1') )

    def test_two(self):
        from session_storage_memcached import SessionStorageMemcached
        from login_biz import Login_Biz
        lb = Login_Biz(Mockup_Account_Biz(), SessionStorageMemcached('127.0.0.1:11211', 'test_session_storage_memcached'))

        lb.login('test_user_1', PASSWORD)
        lb.logout('test_user_2')

        self.assert_( lb.is_logged_in('test_user_1') )
        self.assert_( not lb.is_logged_in('test_user_2') )

    def test_three(self):
        from session_storage_memcached import SessionStorageMemcached
        from login_biz import Login_Biz
        lb = Login_Biz(Mockup_Account_Biz(), SessionStorageMemcached('127.0.0.1:11211', 'test_session_storage_memcached'))

        lb.login('test_user_1', PASSWORD)

    def test_set_by_login(self):
        from session_storage_memcached import SessionStorageMemcached
        from login_biz import Login_Biz

        storage = SessionStorageMemcached('127.0.0.1:11211', 'test_session_storage_memcached')

        lb = Login_Biz(Mockup_Account_Biz(), storage)

        lb.login('test_user_1', PASSWORD)

        storage.set_by_login('test_user_1', { 'STR': 'SSS', 'NUM':22 } )

        d = storage.get_by_login('test_user_1')

        self.assert_( d['STR'] == 'SSS' )
        self.assert_( d['NUM'] == 22 )
        
    def test_set_by_ssid(self):
        from session_storage_memcached import SessionStorageMemcached
        from login_biz import Login_Biz

        storage = SessionStorageMemcached('127.0.0.1:11211', 'test_session_storage_memcached')

        lb = Login_Biz(Mockup_Account_Biz(), storage)

        lb.login('test_user_1', PASSWORD)

        ssid = storage.get_ssid('test_user_1')

        storage.set_by_ssid(ssid, { 'STR': 'SSS', 'NUM':22 } )
        d = storage.get_by_ssid(ssid)

        self.assert_( d['STR'] == 'SSS' )
        self.assert_( d['NUM'] == 22 )

    def test_cleanup(self):
        from session_storage_memcached import SessionStorageMemcached
        from login_biz import Login_Biz

        storage = SessionStorageMemcached('127.0.0.1:11211', 'test_session_storage_memcached')

        lb = Login_Biz(Mockup_Account_Biz(), storage)

        lb.login('test_user_1', PASSWORD)

        storage.set_by_login('test_user_1', { 'STR': 'SSS', 'NUM':22 } )

        d = storage.get_by_login('test_user_1')

        self.assert_( d['STR'] == 'SSS' )

        lb.logout('test_user_1')

        e = None
        try:
            storage.get_by_login('test_user_1')
        except Exception, err:
            e = err

        self.assert_( e.__class__ == KeyError )


if __name__ == '__main__':
    unittest.main()

