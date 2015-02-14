#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from kernel.server import app
from kernel.widget import widget
from bottle import request

@app.post("/upload/preview")
def upload_preview():
    image = request.files.get('upload')

@widget("upload.preview")
def widget():
    pass