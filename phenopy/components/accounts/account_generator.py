import os
from Cheetah.Template import Template
from generator_errors import *

class Account_Postgres_MD5_Salt_Generator(object):

    def __init__(self, path, entity_name='Account', connection_factory='dao.connection_factory', rewrite=False):
        self.path = path
        self.entity_name = entity_name
        self.rewrite = rewrite
        self.connection_factory = connection_factory

    def generate_files(self):
        self.gen_account_dao_file()
        self.gen_account_sql_file()
        self.gen_account_biz_file()

    def gen_account_dao_file(self):
        s = """
from phenopy.sql.postgres import DAO
from phenopy.sql.common import *

class ${CLASS_NAME}(DAO):

    class metadata(object):
        __table__ = '${TABLE}'
        id = column(primary_key=True)
        login = column()
        passwd_hash = column()
        passwd_salt = column()


"""
        klass =  self.dao_class()
        self.write_file(self.mk_fname(self.path, '_dao'), str(Template(s, dict(CLASS_NAME=klass, TABLE=self.entity_name.lower()) )))

    def gen_account_sql_file(self):
        s = """

CREATE SEQUENCE ${TABLE}_pk_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE ${TABLE} (
    id          integer  PRIMARY KEY DEFAULT nextval('${TABLE}_pk_seq'::regclass) NOT NULL,
    login       character varying(30) UNIQUE NOT NULL,
    passwd_hash character varying(34) NOT NULL,
    passwd_salt character(10) NOT NULL
);

"""
        table =  self.entity_name.lower()
        self.write_file(self.mk_sql_fname(self.path), str(Template(s, dict(TABLE=table) )))

    def gen_account_biz_file(self):
        s = """
from __future__ import with_statement
import phenopy.passwords as passwd
from phenopy.sql.common import *
from phenopy.sql.postgres import transaction

from $DAO_CONN_FACT import connect

from $DAO import $DAO_CLASS

class ${CLASS_NAME}:

    def gen_password(self, password=None, length=8, salt_length=10):
        return passwd.generate(password, length, salt_length)

    def is_password_match(self, account, password):
        return passwd.check(password, account.passwd_hash, account.passwd_salt)

    def get_account_by(self, login):
        with connect() as conn:
            dao = ${DAO_CLASS}(conn)
            return dao.get(eq('login', login))

    def create(self, login, passwd_hash, passwd_salt):
        with connect() as conn:
            with transaction(conn):
                dao = ${DAO_CLASS}(conn)
                return dao.create(login=login, passwd_hash=passwd_hash, passwd_salt=passwd_salt)

    def update(self, id, passwd_hash, passwd_salt):
        with connect() as conn:
            with transaction(conn):
                dao = ${DAO_CLASS}(conn)
                return dao.update(eq('id',id),  passwd_hash=passwd_hash, passwd_salt=passwd_salt)

    def delete(self, id):
        with connect() as conn:
            with transaction(conn):
                dao = ${DAO_CLASS}(conn)
                return dao.delete(eq('id',id))

"""
        klass = self.entity_name + 'Biz'
        self.write_file(self.mk_fname(self.path, '_biz'), str(Template(s, dict(CLASS_NAME=klass,
                                                                               DAO=self.mk_mname('_dao'),
                                                                               DAO_CLASS=self.dao_class(),
                                                                               DAO_CONN_FACT=self.connection_factory,
                                                                               ) )))

    def dao_class(self):
        return self.entity_name + 'DAO'

    def mk_mname(self, suffix):
        return self.entity_name.lower() + suffix

    def mk_fname(self, path, suffix):
        return os.path.join(path, self.mk_mname(suffix) + '.py' )

    def mk_sql_fname(self, path):
        return os.path.join(path, self.mk_mname('') + '.sql' )


    def write_file(self, name, content, rewrite=False):
        if not self.rewrite and os.path.exists(name):
            raise FileAlreadyExistsError()

        f = open(name,'w')
        f.write(content)
        f.close()


