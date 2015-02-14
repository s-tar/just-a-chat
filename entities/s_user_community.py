#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from entities.s_community import Community
from entities.s_user import User
from bottle import request


class UserCommunity(Base):
    __tablename__ = 's_user_community'
    ucm_id = Column(Integer, primary_key=True)

    usr_id = Column(Integer, ForeignKey('s_user.usr_id'))
    cm_id = Column(Integer, ForeignKey('s_community.cm_id'))

    user = relationship(User, backref=backref("community_rel"))
    community = relationship(Community, backref=backref("user_rel"))

    ucm_external_id = Column(String(255))
    ucm_additional_data = Column(String(255))