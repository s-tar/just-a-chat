#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

class Community(Base):
    __tablename__ = 's_community'
    cm_id = Column(Integer, primary_key=True)
    cm_alias = Column(String(50))
    cm_name = Column(String(50))