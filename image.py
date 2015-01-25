#coding=utf-8
import logging
import imghdr

from google.appengine.api import images
from basehandler import BaseHandler
from tool import memcache
from tool.datastore import Image
from tool.datastore import User


class ImagePage(BaseHandler):
    def render_img(self,img,img_type):
        self.set_header(
                'Content-Type',
                'image/%s; charset=UTF-8' % img_type
            )
        self.write(img)

    def get(self, imgid):
        user_img = Image.by_id(int(imgid))
        if not user_img:
            self.error(404)
        self.render_img(user_img.img,user_img.img_type)

    @BaseHandler.authenticated
    def post(self, uid):
        post_photo = self.request.files['photo'][0]

        post_user = User.by_id(int(uid))
        if not post_user:
            return self.error(404)
        if post_user.key != self.current_user.key:
            return self.error(403)

        new_img = None
        if self.current_user.img_key:
            new_img = Image.by_id(int(self.current_user.img_key))
            new_img.img = post_photo['body']
            new_img.img_type = imghdr.what(post_photo['filename'],post_photo['body'])
        else:
            new_img = Image(
                    img = post_photo['body'],
                    img_type = imghdr.what(post_photo['filename'],post_photo['body']),
                    parent = Image.parent_key()
                )
        new_img.put()
        
        self.current_user.img_key = str(new_img.key.id())
        self.current_user.put()
        memcache.set(
            'USER_%d'%self.current_user.key.id(),
            self.current_user
        )

        kw = dict()
        kw['img_key'] = new_img.key.id()
        self.render_json(kw)
