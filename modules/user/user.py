#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.server import app
from kernel.validator import Validator
from kernel.db import db
from entities.s_user import User
from entities.s_community import Community
from entities.s_user_community import UserCommunity
from bottle import jinja2_template as template, request, HTTPError
import urllib2
import json
import hashlib
from kernel.socket import Rooms
from kernel.config import config
from kernel.server import files_dir
from kernel.helpers import remove_similar, image_resize, image_thumbnail
import os
import uuid
from kernel.socket import on
from entities.s_chat import Chat

user_path = os.path.abspath(files_dir+"/users/user_{id}")
profile_path = os.path.join(user_path, "profile")
online = {}

@app.post('/user/login/fb')
def login_fb():
    user = None
    data = json.loads(request.forms.data)
    try:
        response = urllib2.urlopen("https://graph.facebook.com/me?fields=first_name,last_name,picture,email&access_token="+data['authResponse']['accessToken'])
        response = json.loads(response.read())
        if response is not None and 'id' in response:
            fb_id = response['id']
            uc = request.db().query(UserCommunity).join(Community)\
                .filter(Community.cm_alias == 'fb', UserCommunity.ucm_external_id == fb_id).first()

            user = uc.user if uc is not None else None
            if user is None:
                email = response['email']

                user = request.db.query(User).filter_by(usr_email=email).first()
                if user is None:
                    user = User(usr_firstname=response['first_name'],
                                usr_lastname=response['last_name'],
                                usr_email=response['email'],
                                usr_photo=response['picture']['data']['url'],
                                usr_photo_s=response['picture']['data']['url'].replace('_q.jpg', '_n.jpg'))

                community = request.db.query(Community).filter_by(cm_alias='fb').first()
                if community is None:
                    community = Community(cm_alias='fb', cm_name='Facebook')

                uc = UserCommunity(user=user, community=community, ucm_external_id=fb_id)
                request.db.add(uc)
                request.db.commit()
                request.db(Chat).join_default(user)
    except HTTPError:
        pass
    return auth(user)


@app.post('/user/login/vk')
def login_vk():
    user = None
    data = json.loads(request.forms.data)
    params = "expire="+str(data['expire']) \
             + "mid="+str(data['mid'])\
             + "secret="+str(data['secret'])\
             + "sid="+str(data['sid'])\
             + str(config['sn']['vk']['app_secret'])
    md5 = hashlib.md5()
    md5.update(params)
    sig = md5.hexdigest()
    if sig == data['sig']:
        try:
            response = urllib2.urlopen("https://api.vk.com/method/getProfiles?uid="+data['mid']+"&fields=uid,photo,photo_big,photo_medium")
            response = json.loads(response.read())
            if response is not None:
                response = response['response'][0]
                vk_id = response['uid']
                uc = request.db().query(UserCommunity).join(Community)\
                    .filter(Community.cm_alias == 'vk', UserCommunity.ucm_external_id == vk_id).first()
                user = uc.user if uc is not None else None
                if user is None:
                    user = User(usr_firstname=response['first_name'],
                                usr_lastname=response['last_name'],
                                usr_photo=response['photo_big'],
                                usr_photo_s=response['photo'])

                    community = request.db.query(Community).filter_by(cm_alias='vk').first()
                    if community is None:
                        community = Community(cm_alias='vk', cm_name='VKontakte')

                    uc = UserCommunity(user=user, community=community, ucm_external_id=vk_id)

                    request.db.add(uc)
                    request.db.commit()
                    request.db(Chat).join_default(user)
        except KeyError, HTTPError:
            pass

    return auth(user)

@app.post('/user/login/native')
def login_native():
    data = request.forms
    v = Validator(data)
    v.field("email").required()
    v.field("password").required()
    if(v.is_valid()):
        data = v.valid_data
        m = hashlib.md5()
        m.update(data.get('password'))
        password_md5 = m.hexdigest()
        user = request.db().query(User).filter(User.usr_email == data.get('email'), User.usr_password == password_md5).first()
        if not user:
            v.add_error('email', 'Неправильный логин или пароль', 'wrong_login')
        else:
            auth(user)
            return {"status": "ok", "reload": True}
    return {"status": "fail",
            "errors": v.errors}


@app.post('/user/registrate')
def registrate():
    data = request.forms
    data['_photo'] = request.files.get('photo')
    v = Validator(data)
    v.field("first_name").required()
    v.field("last_name").required()
    v.field("email").required().email()
    v.field("password").required().length(min=6, message="Длина пароля не менее %(min)d символов")
    v.field("_photo").image()
    if data.get("password") != data.get("repassword"):
        v.add_error('password', 'Пароли не совпадают', 'wrong_repassword')
    if(v.is_valid()):
        data = v.valid_data
        m = hashlib.md5()
        m.update(data.get('password'))
        password_md5 = m.hexdigest()
        user = request.db(User).get_by_email(data['email'])
        if user:
            v.add_error('email', 'Электронный адрес уже используется.', 'email_is_used_already')
        else:
            user = User()
            user.usr_email = data['email']
            user.usr_firstname = data['first_name']
            user.usr_lastname = data['last_name']
            user.usr_password = password_md5
            request.db().add(user)
            request.db.commit()
            request.db(Chat).join_default(user)
            img = data.get("_photo")
            if img is not None:
                path = profile_path.format(id=user.usr_id)
                photo_name = 'photo_'+str(user.usr_id)+"_"+str(uuid.uuid4())+".png"
                thumbnail_name = photo_name.rstrip(".png")+".thumbnail.png"
                if not os.path.exists(path): os.makedirs(path)
                remove_similar(path, photo_name)

                image_path = os.path.join(path, photo_name)
                thumbnail_path = os.path.join(path, thumbnail_name)

                photo = image_thumbnail(img, width=200, height=200)
                photo.save(image_path)

                img.file.seek(0)
                thumbnail = image_thumbnail(img, width=50, height=50)
                thumbnail.save(thumbnail_path)

                user.usr_photo = "/file"+image_path.replace(files_dir, '').replace("\\", '/')
                user.usr_photo_s = "/file"+thumbnail_path.replace(files_dir, '').replace("\\", '/')
                request.db.commit()
            auth(user)
            Rooms.get('session.'+str(request.session().id)).emit('user.login')
            return {"status": "ok"}
    return {"status": "fail",
            "errors": v.errors}

@app.post('/user/logout')
def user_logout():
    user = request.user.get()
    s = request.session()
    if user:
        s.pop('user', None)
        s.persist()
    return {'status': 'ok'}


def auth(user):
    user = request.user.set(user)
    if user:
        return {'status': 'ok'}
    else:
        return {'status': 'fail'}

@on('user.logout')
def user_logout(socket):
    s = socket.session()
    user = socket.user.get()
    if user:
        socket.user.set(None)
        for sid, sock in socket.room('session.'+str(s.id)).sockets().items():
            sock.leave('user.'+str(user.usr_id))
        socket.room('session.'+str(s.id)).emit('user.logout', {'user': user.public_data()})
        if not online.get(user.usr_id, {}):
            socket.all.emit('user.offline', {'user': user.public_data()})



@on('user.login')
def user_login(socket):
    s = socket.session()
    user = socket.user.get()
    if user:
        for sid, sock in socket.room('session.'+str(s.id)).sockets().items():
            sock.join('user.'+str(user.usr_id))
        socket.all.emit('user.online', {'user': user.public_data()})
        socket.room('session.'+str(s.id)).emit('user.login', {'user': user.public_data()})
        online[user.usr_id] = socket.room('user.'+str(user.usr_id)).sockets()


@on('connect')
def user_connect(socket):
    user = socket.user.get()
    if user is not None:
        connections = socket.room('user.'+str(user.usr_id)).sockets()
        online[user.usr_id] = connections
        if len(connections) == 0:
            socket.all.emit('user.online', {'user': user.public_data()})
        socket.join('user.'+str(user.usr_id))
    return False

@on('disconnect')
def user_disconnect(socket):
    user = socket.user.get()
    if user is not None:
        socket.leave('user.'+str(user.usr_id))
        connections = socket.room('user.'+str(user.usr_id)).sockets()
        if len(connections) == 0:
            if not online.get(user.usr_id, {}):
                socket.all.emit('user.offline', {'user': user.public_data()})
