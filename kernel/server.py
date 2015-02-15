#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

import bottle
import datetime
from kernel.widget import get as loadWidget
from kernel.helpers import is_ajax
from bottle import default_app, Bottle, route, static_file, ServerAdapter, Jinja2Template, request, error, redirect, jinja2_template as template
from kernel.session import Session
from beaker.middleware import SessionMiddleware
from kernel.user import User
import time
import kernel.db
import sys
import os

bottle.debug(True)
app = application = Bottle()
reload(sys)
sys.setdefaultencoding('UTF8')
template_path = './templates/default/'
bottle.TEMPLATE_PATH.insert(0, template_path)

def run(run=True):
    global app
    # redistogo_url = os.getenv('REDISTOGO_URL', None)
    # if redistogo_url == None:
    #   redis_url = '127.0.0.1:6379'
    # else:
    #   redis_url = redistogo_url
    #   redis_url = redis_url.split('redis://redistogo:')[1]
    #   redis_url = redis_url.split('/')[0]
    #   REDIS_PWD, REDIS_HOST = redis_url.split('@', 1)
    #   redis_url = "%s?password=%s" % (REDIS_HOST, REDIS_PWD)
    # session_opts = {
    #     'session.type': 'redis',
    #     'session.url': redis_url,
    #     'session.key': 'just_a_chat',
    #     'session.auto': True, }
    session_opts = {
        'session.type': 'file',
        'session.data_dir': './temp/sessions',
        'session.cookie_expires': 7*24*60*60,
        'session.auto': True}
    
    from kernel.socket import SocketIOServer

    class BeforeRequestMiddleware(object):
        def __init__(self, app):
            self.app = app

        def __call__(self, e, h):
            e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
            return self.app(e, h)

    Jinja2Template.defaults = {
        'widget': loadWidget,
        'is_ajax': is_ajax,
        'modules': kernel.module.modules,
        'datetime': datetime
    }
    Jinja2Template.settings = {
        'filters': {
            'nl2br': lambda value: value.replace('\n', '<br>\n')
        }
    }


    @app.route('/static/<path:path>')
    def static(path):
        return static_file(path, './templates/default/static/')

    @app.route('/file/<path:path>')
    def file(path):
        return static_file(path, './files/')

    @app.post('/widget/<name:path>')
    def widget(name):
        try:
            data = request.json['data'] if request.json is not None and 'data' in request.json else {}
            return loadWidget(name, data, wrap=False)
        except ValueError:
            bottle.response.status = 404


    @app.error(404)
    def error404(error):
        return template("404")

    @app.hook('before_request')
    def before_request():
        request.session = Session(request)
        request.db = kernel.db.Database()
        request.user = User(request.session, request.db)
        Jinja2Template.defaults['user'] = request.user

    @app.hook('after_request')
    def after_request():
        request.db().close()


    app = BeforeRequestMiddleware(app)
    app = SessionMiddleware(app, session_opts)
    

    if run:
        #bottle.run(app, host='192.168.1.2', port=3000)
        return SocketIOServer(('192.168.1.2', 3000), app).serve_forever()


def get_environment():
    if request.environ['PATH_INFO'].startswith('/admin/') or request.environ['PATH_INFO'] == '/admin':
        return 'admin'
    else:
        return 'site'

files_dir = os.path.abspath("./files/")
from modules import *

__all__ = ["app", "session", "files_dir"]