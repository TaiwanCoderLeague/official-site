#coding=utf-8
import logging

from basehandler import BaseHandler
from tool.datastore import Message
from tool.datastore import User


class MessagePage(BaseHandler):
    def get_roomname(self):
        return 'Class '+'TWCL'[self.current_user.chatclass]

    @BaseHandler.authenticated
    def get(self,path):
        kw = dict()
        if path:
            room_user = User.by_account(path)
            if not room_user:
                return self.redirect('/message')
            kw['roomname'] = self.current_user.name
            kw['message'] = Message.by_ancestor(room_user.key)
            kw['face_url'] = '/static/img/autoface.png'
            if room_user.img_key:
                kw['face_url'] = '/img/'+room_user.img_key
            kw['path'] = '/'+path
            kw['user_key'] = self.current_user.key.id()
            kw['self_message_page'] = room_user.key==self.current_user.key
            self.render('message.html',**kw)
        else:
            kw['roomname'] = self.get_roomname()
            kw['message'] = Message.by_ancestor(Message.room_key(kw['roomname']))
            kw['face_url'] = '/static/img/autoface.png'
            kw['path'] = ''
            kw['user_key'] = ''
            kw['self_message_page'] = False
            self.render('message.html',**kw)

    @BaseHandler.authenticated
    def post(self,path):
        kw = dict()
        kw['content'] = self.get_argument(name='content')
        if path:
            room_user_key = User.by_account(path,keys_only=True)
            if not room_user_key:
                return self.error(403)
            kw['parent'] = room_user_key
            kw['author'] = self.current_user.key
            new_message = Message(**kw)
            new_message.put()
            # self.render_json(dict(content=kw['content']))
            self.get(path)
        else:
            kw['parent'] = Message.room_key(self.get_roomname())
            kw['author'] = self.current_user.key
            new_message = Message(**kw)
            new_message.put()
            # self.render_json(dict(content=kw['content']))
            self.get(path)
