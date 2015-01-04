#coding=utf-8

# "posts.py" 4 type of post: Question, Discus, Technology, Amazing.

import logging

from tool.datastore import Post
from basehandler import Basehandler


def add_new_post(**kw):
    pass


class PostPage(Basehandler):
    def get(self):
        return self.error(404)

    @tornado.web.authenticated
    def post(self):
        pass
