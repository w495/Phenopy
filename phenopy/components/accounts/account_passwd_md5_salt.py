
import phenopy.passwords as passwd

class Password_MD5_Salt(object):

    def gen_password(self, password=None, length=8, salt_length=10):
        return passwd.generate(password, length, salt_length):

    def gen_password_hash(self, s):
        pass

    def is_password_match(self, account, password):
        return passwd.check(password, account.passwd_hash, account.passwd_salt)

