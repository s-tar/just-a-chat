#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'


class Entity():
    def t(self, attr, editable=False, default=None):
        val = getattr(self, attr)
        if val is None: val = default
        return val

    def as_dict(self, translated=False):
        d = {}
        for c in self.__table__.columns:
            val = self.t(c.name, translated, getattr(self, c.name))
            d[c.name] = str(val) if val is not None else ''
        return d

    @classmethod
    def get_by_id(cls, conn, id):
        return conn.query(cls).filter(cls.id == id).first()
