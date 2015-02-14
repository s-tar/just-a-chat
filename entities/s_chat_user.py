#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class ChatUser(Base):
    __tablename__ = 's_chat_user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('s_user.usr_id'))
    chat_id = Column(Integer, ForeignKey('s_chat.id'))