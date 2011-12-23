from errors import *

class Session_Storage_Base(object):

    def kill(self, login):
        raise Exception()

    def add(self, login, data = {}):
        raise Exception()

    def get_by_login(self, login):
        raise Exception()

    def set_by_login(self, login, data):
        raise Exception()

    def get_by_ssid(self, ssid):
        raise Exception()

    def set_by_ssid(self, ssid, data):
        raise Exception()

class Login_Biz(object):
    
    def __init__(self, account_biz, session_storage):
        self.acc = account_biz
        self.storage = session_storage

    def login(self, login, password):
        self.logout(login)
        acc = self.acc.get_account_by(login=login)

        if acc is None:
            raise AccountNotFound()

        if not self.acc.is_password_match(acc, password):
            raise BadLoginOrPassword()

        self.storage.add(login, {})

    def logout(self, login):
        self.storage.kill(login)

    def is_logged_in(self, login):
        try:
            self.storage.get_by_login(login)
        except KeyError:
            return False

        return True 

