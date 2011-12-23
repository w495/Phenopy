
PASSWORD='PassWorD111'


class Mockup_Account(object):
    
    def __init__(self, **kw):
        self.__dict__.update(kw)

    @property
    def password_hash(self):
        return hash(self.password)

class Mockup_Account_Biz():


    accounts = {
         'test_user_1' : Mockup_Account(login='test_user_1', password=PASSWORD)
        ,'test_user_2' : Mockup_Account(login='test_user_2', password=PASSWORD)
    }

    def get_account_by(self, login):
        return (self.accounts.has_key(login) and self.accounts[login]) or None

    def gen_password_hash(self, s):
        return hash(s)

    def is_password_match(self, acc, password):
        return hash(acc.password) == hash(password)

class Mockup_Session_Storage(object):
    
    def __init__(self):
        self.storage = {}

    def kill(self, login):
        if self.storage.has_key(login):
            del self.storage[login]

    def add(self, login, data = {}):
        self.storage[login] = data

    def get_by_login(self, login):
        return self.storage[login]

