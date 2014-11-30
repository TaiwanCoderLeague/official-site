from google.appengine.api import memcache
from datetime import datetime,timedelta

def get(k):
    return memcache.get(k)
def set(k,v):
    return memcache.set(k,v)
def delete(k):
    return memcache.delete(k)
def flush():
    return memcache.flush_all()
def age_get(k):
    r = get(k);
    if r:
        val,age = r
    else:
        val,age = None,0
    return val,age
def age_set(k,v,tag):
    val,age = age_get(k)
    if age != tag:
        return False
    save_time = datetime.utcnow()
    set(k,(v,save_time))
    return True