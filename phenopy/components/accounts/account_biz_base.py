

class Account_Biz_Base(object):
    ''' Base interface for accounting '''

    def get_account_by(self, login):
        pass

    def gen_password_hash(self, s):
        pass

    def is_password_match(self, account, password):
        pass

