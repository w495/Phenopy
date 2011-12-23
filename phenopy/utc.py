from datetime import datetime
import time, calendar

def to_utc(the_datetime):
    return datetime.utcfromtimestamp( time.mktime(the_datetime.timetuple()) )

def from_utc(the_datetime):
    return datetime.fromtimestamp(calendar.timegm(the_datetime.timetuple()))

