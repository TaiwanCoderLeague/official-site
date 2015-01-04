#coding=utf-8

# "posts.py" 4 type of post: Question, Discus, Technology, Amazing.

import logging

from tornado.web import authenticated
from tool.datastore import Post
from basehandler import BaseHandler


def add_new_post(**kw):
    pass


class PostPage(BaseHandler):
    def get(self):
        return self.error(404)

    @authenticated
    def post(self):
        pass
