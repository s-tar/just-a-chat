#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'


class Session(object):
    __sessions = {}

    def __init__(self, environ):
        self.__id = environ.get('bottle.request.cookies', {}).get('beaker.session.id')
        if self.__id not in self.__class__.__sessions:
            self.__class__.__sessions[self.__id] = environ.get('beaker.session')

    def __call__(self):
        return self.get()

    def id(self):
        return self.__id

    def session(self):
        return self.get()

    def get(self):
        return self.__class__.__sessions.get(self.__id, {})

    def delete(self):
        if self.id in self.__class__.__sessions:
            del self.__class__.__sessions[self.id]