#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from kernel.server import app
from kernel.widget import *
from bottle import jinja2_template as template, jinja2_view as view
from kernel.config import config


@app.route("/config/sn")
def config_sn():
    return {
        'vk': {
            'app_id': config['sn']['vk']['app_id']
        },
        'fb': {
            'app_id': config['sn']['fb']['app_id']
        }
    }


@widget('main.popup')
def widget_main_popup():
    return template('widgets/popup')