#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'


config = {
    'common' : {
        'siteTitle': "Chaty",
        'logoImage': "/images/logo.png"
    },
    'cookie': {
        'secret': 'SuperSecretText'
    },
    'db': {
        'type': 'postgres',
        'host': "localhost",
        'db': 'just_a_chat',
        'port': 5432,
        'username': 'postgres',
        'password': '',
    },
    'sn': {
        'vk': {
            'app_id': 4783971 ,
            'app_secret': 'EOlMVl0XFBOQPcH2RKsz'
        },
        'fb': {
            'app_id': '913186355380238' ,
            'app_secret': 'ab496243bcc6b35da1cf25b4a4494849'
        }
    }
}
