import datetime
from datetime import time
from timezonefinder import TimezoneFinder
from pytz import timezone


def check_timezone_gps(locations):
    tf = TimezoneFinder(in_memory=True)
    TimezoneFinder.using_numba()
    return tf.timezone_at(lng=locations.longitude, lat=locations.latitude)

def check_timezone(tz):
    if is_number(tz):
        tz = int(tz) * (-1)
        if tz >= -14 and tz <= 12:
            if tz > 0 :
                tz = "{}{}".format("+", str(tz))
            else:
                tz = str(tz)
            return "Etc/GMT{}".format(tz)
    return False

def is_number(s):
    try:
        int(s)
        return True
    except:
        return False

def loc_time(tz):
    now = datetime.datetime.now()
    local = timezone(tz)
    local = now.astimezone(local)
    return local

def date_is_correct(dt):
    try:
        dt = [int(item) for item in dt]
        datetime.date(dt[2], dt[1], dt[0])
        return True
    except:
        return False

def weekday_is_correct(wd):
    try:
        wd = [int(item) for item in wd]
        return True
    except:
        return False
