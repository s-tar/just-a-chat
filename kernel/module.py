#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from kernel.server import app
from functools import wraps

modules = []
class Module(object):
    def __init__(self, name="unknown", route="", is_admin=False, group=""):
        self.name = self.__class__.__name__
        self.name = name
        self._route = route
        self.index = route
        self.is_admin = is_admin
        self.group = group
        modules.append(self)

    def route(self, route, is_index=False, *args, **kargs):
        route = self._route + route
        if is_index:
            self.index = route

        def wrapper(fn):
            return app.route(route, *args, **kargs)(fn)
        return wrapper

    def post(self, route, *args, **kargs):
        def wrapper(fn):
            return app.post(self._route + route, *args, **kargs)(fn)
        return wrapper

    def get(self, route, *args, **kargs):
        def wrapper(fn):
            return app.get(self._route + route, *args, **kargs)(fn)
        return wrapper