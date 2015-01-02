#coding=utf-8
import facebook
import memcache
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
def check_user(name,passward):
    pass

def new_user(**kw):
    pass
