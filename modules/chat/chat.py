#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from kernel.module import Module
from kernel.server import app
from bottle import jinja2_template as template, request
from entities.s_chat import Chat
from entities.s_message import Message
from kernel.validator import Validator
from kernel.socket import Rooms
import opengraph
import urlparse
import kernel.widget

module = Module('chat', route="/chat")

@app.route('/')
@app.route('/chat/<chat_id:int>')
def main(chat_id=None):
    user = request.user.get()
    if user:
        chats = request.db(Chat).get_all_by_user(user)
        current_chat = request.db(Chat).get_by_id(chat_id) if chat_id else None
        return template('page', {'content': template('chat/main', {
            'chats': chats,
            'chat_id': chat_id,
            'current_chat': current_chat,
            'current_is_new': current_chat and current_chat not in chats
        })})

    return template('page', {'content': template('index')})


@module.post('/new')
def new_chat():
    user = request.user.get()
    if user:
        data = request.forms
        v = Validator(data)
        v.field("chat_name").required(message='Назовите как-то чат')
        if v.is_valid():
            data = v.valid_data
            chat = Chat()
            chat.name = data.get("chat_name")
            chat.members.append(user)
            request.db.add(chat)
            request.db.flush()
            request.db.commit()
            Rooms.get('user.'+str(user.usr_id)).emit('chat.new', {
                'chat': chat.as_dict(),
                'chat_item': kernel.widget.get('chat.item', {'chat': chat})})
            return {"status": "ok"}

    return {"status": "fail", "errors": v.errors}


@module.post('/<chat_id:int>/join')
def join_chat(chat_id=None):
    user = request.user.get()
    if user:
        chat = request.db(Chat).get_by_id(chat_id)
        if chat and user not in chat.members:
            chat.members.append(user)
            request.db.add(chat)
            request.db.commit()
            Rooms.get('user.'+str(user.usr_id)).emit('chat.join', { "chat": chat.as_dict(),
                    "chat_item": kernel.widget.get('chat.item', {'chat': chat})})

            new_message(request.db, chat, '%s %s присоединился(сь) к чату.' % (user.usr_firstname, user.usr_lastname), user, True)
            return {"status": "ok",
                    "chat": chat.as_dict(),
                    "chat_item": kernel.widget.get('chat.item', {'chat': chat}),
                    "messages": kernel.widget.get('chat.messages', {'chat_id': chat.id})
            }

    return {"status": "fail"}


@module.post('/<chat_id:int>/leave')
def leave_chat(chat_id=None):
    user = request.user.get()
    if user:
        chat = request.db(Chat).get_by_id(chat_id)
        if chat:
            chat.members.remove(user)
            if len(chat.members) == 0:
                chat.deleted = True
            request.db.add(chat)
            request.db.commit()
            new_message(request.db, chat, '%s %s покинул(а) чат.' % (user.usr_firstname, user.usr_lastname), user, True)
            return {"status": "ok"}

    return {"status": "fail"}


@module.post('/new_message')
def new_message_route():
    user = request.user.get()
    if user:
        data = request.forms
        v = Validator(data)
        v.field("chat_id").integer()
        if v.valid_data.get('chat_id'):
            data = v.valid_data
            chat = request.db(Chat).get_by_id(data.get('chat_id'))
            if chat:
                text = data.get('message').strip()
                new_message(request.db, chat, text, user)
                return {"status": "ok"}
    return {"status": "fail"}


@module.post('/search')
def search():
    user = request.user.get()
    text = request.forms.get('text')
    chats = request.db().query(Chat).filter(Chat.deleted == False, Chat.name.like(text+'%'), ~Chat.members.contains(user)).all()
    return {
        'chats': [c.as_dict() for c in chats],
        'chat_items': [kernel.widget.get('chat.item', {'chat': chat}) for chat in chats]
    }

def to_url(text):
    text = 'http://'+text if text.startswith('www.') else text
    return text if text.startswith('http://') or text.startswith('https://') else None


def new_message(db, chat, text, user, system=False):
    data = None
    url = to_url(text)
    if url:
        try:
            og = opengraph.OpenGraph(url=url)
            text = url
            data = str(og if og.is_valid() else {})
        except:
            data = str({})

    message = Message()
    message.chat = chat
    message.text = text
    message.data = data
    message.sender = user
    message.is_system = system
    chat.messages.append(message)

    db.add(chat)
    db.flush()
    db.commit()
    for member in chat.members:
        Rooms.get('user.'+str(member.usr_id)).emit('chat.new_message', {
            'is_sender': member.usr_id == user.usr_id,
            'message': message.as_dict(),
            'message_item': kernel.widget.get('chat.message', {'message': message})})