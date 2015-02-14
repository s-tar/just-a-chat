#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.widget import widget
from bottle import request, jinja2_template as template
from entities.s_chat import Chat
import ast

@widget('chat.messages')
def messages_widget(chat_id):
    chat = request.db(Chat).get_by_id(chat_id)
    user = request.user.get()
    return template('chat/messages', {'chat': chat, 'is_member': user in chat.members})


@widget('chat.message')
def message_widget(message):
    try:
        url_html = template('chat/url_preview', {'url': message.text, 'og': ast.literal_eval(message.data)})
    except:
        url_html = ''
    return template('chat/message', {'message': message, 'url_html': url_html})


@widget('chat.item')
def chat_item_widget(chat, is_active=False):
    return template('chat/chat_item',{'chat':chat, 'is_active': is_active}) if chat else ''