import psycopg2
from contextlib import contextmanager
import psycopg2.extensions as pge
from phenopy.config import configuration
import os

from DBUtils.PooledDB import PooledDB
_pool = PooledDB(psycopg2, 10, database='''phenopy_test_db''')

@contextmanager
def connect(isolation_level=pge.ISOLATION_LEVEL_READ_COMMITTED):
    global _pool
    _conn = _pool.connection()
    try:
        yield _conn
    finally:
        pass

