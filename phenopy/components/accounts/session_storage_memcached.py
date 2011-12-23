import sys, os, md5, random, datetime, string
from login_biz import Session_Storage_Base

import memcache

class StorageError(Exception):
    pass

class SessionDesc(object):
    def __init__(self, ssid):
        self.ssid = ssid

class SessionStorageMemcached(Session_Storage_Base):

    def __init__(self, memcached_uri, prefix, expire_sec=86400*7*4, debug = False):
        self.prefix = prefix
        self.session_expiration = expire_sec
        self.client = memcache.Client([memcached_uri], debug=debug)

    def kill(self, login):
        ssid = self.get_ssid(login)
        if ssid is not None:
            self.client.delete(ssid)
            self.client.delete(self.s_key(login))

    def add(self, login, data = {}):
        ssid = self.gen_ssid(login)

        if not self.client.set(self.s_key(login), SessionDesc(ssid), self.session_expiration):
            raise StorageError()

        if not self.client.set(ssid, data, self.session_expiration):
            raise StorageError()

    def get_by_login(self, login):
        ssid = self.get_ssid(login)
        if ssid is None:
            raise KeyError()
        data =  self.client.get(ssid)
        if data is None:
            raise KeyError()
        return data

    def set_by_login(self, login, data):
        ssid = self.get_ssid(login)
        if not self.client.set(ssid, data, self.session_expiration):
            raise StorageError()

    def get_by_ssid(self, ssid):
        data =  self.client.get(ssid)
        if data is None:
            raise KeyError()
        return data

    def set_by_ssid(self, ssid, data):
        if not self.client.set(ssid, data, self.session_expiration):
            raise StorageError()

    def s_key(self, s):
        return ''.join((self.prefix, '__', s))

    def gen_ssid(self, login):
        s = "".join([ login,
                      datetime.datetime.now().isoformat(),
                      "".join(random.sample(string.ascii_letters,10)) ])
        return str(md5.md5(s).hexdigest())

    def get_ssid(self, login):
        sd = self.client.get(self.s_key(login))
        if sd is not None:
            return sd.ssid
        return None

