#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
import datetime
from entities.entity import Entity

class Message(Base, Entity):
    __tablename__ = 's_message'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    data = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('s_user.usr_id'))
    chat_id = Column(Integer, ForeignKey('s_chat.id'))
    is_system = Column(Boolean(create_constraint=False), default=False)

    sender = relationship("User", backref=backref("messages", uselist=True), uselist=False)
    chat = relationship("Chat", backref=backref("messages"), uselist=False)