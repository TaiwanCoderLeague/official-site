#coding=utf-8
import logging
import imghdr

from google.appengine.api import images
from basehandler import BaseHandler
from tool import memcache
from tool import datastore
from tool.datastore import Image


class ImagePage(BaseHandler):
    def render_img(self,img,img_type):
        self.set_header(
                'Content-Type',
                'image/%s; charset=UTF-8' % img_type
            )
        self.write(img)

    def get(self, urlsafe):
        compression = self.get_argument(name='compression',default='')
        
        user_img = datastore.get_from_urlsafe(urlsafe)
        if not user_img:
            self.error(404)

        if compression == '32*32':
            pass
        else:
            pass
        self.render_img(user_img.img,user_img.img_type)

    @BaseHandler.authenticated
    def post(self, urlsafe):
        post_photo = self.request.files['photo'][0]

        post_user = datastore.get_from_urlsafe(urlsafe)
        if not post_user:
            return self.error(404)
        if post_user.key != self.current_user.key:
            return self.error(403)

        new_img = None
        if self.current_user.img_key:
            new_img = self.current_user.img_key.get()
        if not new_img:
            new_img = Image(parent = Image.parent_key())
        new_img.img = post_photo['body']
        new_img.img_type = imghdr.what(post_photo['filename'],post_photo['body'])
        new_img.put()

        if not self.current_user.img_key:
            self.current_user.img_key = new_img.key
            self.current_user.put()
            memcache.set(
                'USER_%d'%self.current_user.key.id(),
                self.current_user
            )

        kw = dict()
        kw['img_key'] = new_img.key.urlsafe()
        self.render_json(kw)
