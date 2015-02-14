#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from entities.entity import Entity
from entities.s_chat_user import ChatUser

class Chat(Base, Entity):
    __tablename__ = 's_chat'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    deleted = Column(Boolean(create_constraint=False), default=False)

    members = relationship("User", secondary='s_chat_user', backref=backref('chats'), uselist=True)

    @staticmethod
    def get_all_by_user(conn, user):
        return conn.query(Chat).filter(Chat.members.contains(user), Chat.deleted == False).order_by(Chat.id.desc()).all()

    @staticmethod
    def join_default(conn, user):
        chat = Chat.get_by_id(conn, 1)
        if not chat:
            chat = Chat()
            chat.name = 'Demo chat'
        chat.members.append(user)
        conn.add(chat)
        conn.commit()
