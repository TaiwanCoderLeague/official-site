#coding=utf-8
import facebook
import memcache
import random
import hashlib
import string
import re
import logging

from datastore import User
from config import APP_Key


# FB user function
def get_fb_cookie(cookies):
    return facebook.get_user_from_cookie(cookies,
                                    APP_Key.get('FACEBOOK_APP_ID'),
                                    APP_Key.get('FACEBOOK_APP_SECRET'))


def check_facebook_user(fb_cookie):
    user = User.by_fid(str(fb_cookie['uid']))
    if not user:
        return None
    elif user.access_token != fb_cookie["access_token"]:
        user.access_token = fb_cookie["access_token"]
        user.put()
    return user


def new_facebook_user(fb_cookie):
    graph = facebook.GraphAPI(fb_cookie["access_token"])
    profile = graph.get_object("me")
    user = User(
        parent=User.parent_key(),
        fbuser = True,
        fid = str(profile["id"]),
        name = profile["name"],
        img_key = '',
        profile_url = profile["link"],
        access_token = fb_cookie["access_token"]
    )
    user.put()
    return user


# normal user function
def make_salt():
    return ''.join(random.choice(string.letters) for i in xrange(5))


def hash_passward(account,passward,salt=''):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(account+passward+salt).hexdigest()
    return '%s,%s'%(h,salt)


def get_user(account):
    return User.by_account(account)


def check_user(user,passward):
    salt = user.passward.split(',')[1]
    return user.passward == hash_passward(user.account,passward,salt)


def match_string(string,sr):
    return re.compile(sr).match(string)


def new_user(**kw):
    user = User(
            parent=User.parent_key(),
            name = kw['account'],
            img_key = '',
            account = kw['account'],
            passward = hash_passward(kw['account'],kw['passward']),
            fbuser = False,
        )
    user.put()
    return user.key.id()
