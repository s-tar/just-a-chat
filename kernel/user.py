#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from entities.s_user import User as UserEntity

class User(object):
    def __init__(self, session, db):
        self._session = session
        self._user = None
        self._db = db

    def get(self):
        if not self._session():
            return None
        id = self._session().get('user', {}).get('id', None)
        if not self._user and id:
            self._user = self._db(UserEntity).get_by_id(id)
        return self._user

    def set(self, user):
        s = self._session()

        if user:
            s.setdefault('user', {})['id'] = user.usr_id
            s.persist()
            self._user = user
        else:
            if 'user' in s:
                del s['user']
            s.persist()
            self._user = None
        return self._user

    def role(self, role):
        if self._user:
            for _role in self._user.roles:
                if _role.usrr_code == role or _role.usrr_code == 'superadmin':
                    return True
        return False