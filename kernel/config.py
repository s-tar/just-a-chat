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
        'password': 'gbgbcrf',
    },
    'sn': {
        'vk': {
            'app_id': 3775380 ,
            'app_secret': '6skSVjVfzcCJLCdx9NUg'
        },
        'fb': {
            'app_id': '276442509075653' ,
            'app_secret': '931b421a32c44cbcebdccf3063bdb649'
        }
    }
}
