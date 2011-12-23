import unittest
import sys, os, inspect

from phenopy.misc import add_relative_module_path

from mockup_login import *



class TestLogin(unittest.TestCase):
    
    def setUp(self):
        add_relative_module_path(self.__class__, '../src')

    def testlogin_valid(self):
        from login_biz import Login_Biz
        lb = Login_Biz(Mockup_Account_Biz(), Mockup_Session_Storage())
        lb.login('test_user_1', PASSWORD)
        pass

    def testlogin_invalid_login(self):
        from login_biz import Login_Biz
        from errors import AccountNotFound
        lb = Login_Biz(Mockup_Account_Biz(), Mockup_Session_Storage())

        e = None
        try:
            lb.login('test_user_10000', PASSWORD)
        except Exception, catched:
            e = catched

        self.assert_( e.__class__ == AccountNotFound )

    def testlogin_invalid_password(self):
        from login_biz import Login_Biz
        from errors import BadLoginOrPassword
        lb = Login_Biz(Mockup_Account_Biz(), Mockup_Session_Storage())

        e = None
        try:
            lb.login('test_user_1', PASSWORD.lower())
        except Exception, catched:
            e = catched

        self.assert_( e.__class__ ==  BadLoginOrPassword)

    def testis_logged_in(self):
        from login_biz import Login_Biz
        lb = Login_Biz(Mockup_Account_Biz(), Mockup_Session_Storage())
        lb.login('test_user_1', PASSWORD)
        self.assert_( lb.is_logged_in('test_user_1') )


    def testis_not_logged_in(self):
        from login_biz import Login_Biz
        lb = Login_Biz(Mockup_Account_Biz(), Mockup_Session_Storage())
        self.assert_( not lb.is_logged_in('test_user_2') )

if __name__ == '__main__':
    unittest.main()

