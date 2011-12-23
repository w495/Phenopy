import new,re
from datetime import datetime, date, timedelta
import sys, os

import inspect

def any_class(name):
    o = new.classobj(name, (object,), {'__init__':lambda self,**kw: self.__dict__.update(kw)})
    module = inspect.getmodule(o)
    if not getattr(module, o.__name__, None):
        setattr(module, o.__name__, o)
    return getattr(module, o.__name__)

def datetime_from_iso_str(s):
    return datetime(*tuple([int(x) for x in re.split(r'\D', s)]))

def date_from_iso_str(s):
    return date(*tuple([int(x) for x in re.split(r'\D', s)]))

def attr_exists(o, a):
    return hasattr(o, a) and getattr(o, a)


def guard(object):
    def __enter__(o):
        self.o = o

    def __exit__(o):
        del self.o

 
class fancy_time_delta(object):
    def __init__(self, n1, n2):
        delta =  n2 - n1
        self.days = delta.days
        self.hours = delta.seconds / 3600
        self.minutes = (delta.seconds % 3600 ) / 60

def get_abs_module_path(obj):
    return os.path.realpath(os.path.split(inspect.getfile(obj))[0:-1][0])

def add_relative_module_path(obj, rel_path):
    sys.path.append(os.path.realpath(os.path.join(os.path.split(inspect.getfile(obj))[0:-1][0],rel_path)))

