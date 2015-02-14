#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base, db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from entities.s_user_role import UserRole
from bottle import request
from entities.entity import Entity

class User(Base, Entity):
    __tablename__ = 's_user'
    usr_id = Column(Integer, primary_key=True)
    usr_email = Column(String(50))
    usr_password = Column(String(50))
    usr_firstname = Column(String(50))
    usr_lastname = Column(String(50))
    usr_photo = Column(String(255))
    usr_photo_s = Column(String(255))


    communities = relationship("Community", secondary='s_user_community', backref=backref('users'), uselist=True)
    roles = relationship(UserRole, backref=backref('user'), uselist=True)

    def public_data(self):
        return {
            'id': self.usr_id,
            'first_name': self.usr_firstname,
            'last_name': self.usr_lastname,
            'photo': self.usr_photo,
            'photo_s': self.usr_photo_s
        }

    @staticmethod
    def get_by_id(conn, id):
        return conn.query(User).filter(User.usr_id == id).first()

    @staticmethod
    def get_by_email(conn, email):
        return conn.query(User).filter(User.usr_email == email).first()