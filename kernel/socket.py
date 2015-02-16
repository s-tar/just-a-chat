#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from bottle import request
from kernel.server import app
from kernel.session import Session
from kernel.user import User
import inspect
import kernel.db
import sys

routes = {}

@app.route('/socket.io/<path:path>')
def socketio(path):
    from bottle import default_app
    socketio_manage(request.environ, {'/main': MainNamespace}, request)


class Actions():
    def __init__(self, container, socket):
        self.socket = socket
        self.container = container

    def emit(self, event, *args, **kwargs):
        for id, socket in self.container.sockets.items():
            socket.emit(event, *args, **kwargs)
        return self

    def broadcast(self, event, *args, **kwargs):
        for id, socket in self.container.sockets.items():
            if id != self.socket.socket.sessid:
                socket.emit(event, *args, **kwargs)
        return self

    def sockets(self):
        return self.container.sockets


class Rooms():
    _rooms = {}

    @classmethod
    def all(cls):
        return cls._rooms

    @classmethod
    def get(cls, name):
        room = cls._rooms.get(name, Room(name))
        return Actions(room, cls)


class Room():
    def __init__(self, name=None):
        self.sockets = {}
        self.name = name

    def add(self, socket):
        rooms = getattr(socket, 'rooms', None)
        if rooms is None: setattr(socket, 'rooms', {})
        socket.rooms[self.name] = self
        return self.sockets.setdefault(socket.socket.sessid, socket)

    def remove(self, socket):
        rooms = getattr(socket, 'rooms', None)
        if rooms is None: setattr(socket, 'rooms', {})
        socket.rooms.pop(self.name, None)
        return self.sockets.pop(socket.socket.sessid, None)

# rooms = {}


class Sockets():
    def __init__(self):
        self.sockets = {}

    def add(self, socket):
        return self.sockets.setdefault(socket.socket.sessid, socket)

    def remove(self, socket):
        return self.sockets.pop(socket.socket.sessid, None)


sockets = Sockets()


class MainNamespace(BaseNamespace):
    def process_event(self, packet):
        try:
            name = packet['name']
            data = packet['args'][0] if packet.get('args') else []
            fn_data = {'socket': self}
            self.db = kernel.db.Database()
            self.user = User(self.session, self.db)
            if routes.get(name):
                for fn in routes.get(name):
                    specs = inspect.getargspec(fn)
                    func_args = specs.args
                    for arg in func_args:
                        if arg is not 'socket':
                            if arg is 'data':
                                fn_data[arg] = data
                            else:
                                if isinstance(data, dict):
                                    val = data.get(arg)
                                    if val:
                                        fn_data[arg] = val
                                        del data[arg]
                                elif isinstance(data, list):
                                    fn_data[arg] = data.pop(0) if len(data) else []
                                else:
                                    fn_data[arg] = data
                                    data = None

                    if isinstance(data, dict) and specs.keywords:
                        fn_data = dict(data.items()+fn_data.items())
                    if len(func_args) == 0:
                        fn()
                    else:
                        fn(**fn_data)
        finally:
            self.db().close()


    def call_method(self, method_name, packet, *args):
        if method_name is 'recv_connect': self.recv_connect()

    def initialize(self):
        print '------------------->', self.environ.get('bottle.request.cookies', {}).get('beaker.session.id')
        # for key,val in self.environ.items():
        #     print key,'  ->  ', val
        self.session = Session(self.request)
        self.process_event({'name': 'initialize'})

    def recv_connect(self):
        sockets.add(self)
        self.process_event({'name': 'connect'})

    def recv_disconnect(self):
        s = sockets.remove(self)
        if s: self.process_event({'name': 'disconnect'})

    def join(self, name):
        room = Rooms.all().setdefault(name, Room(name))
        room.add(self)
        return room

    def leave(self, name):
        room = Rooms.all().setdefault(name, Room(name))
        room.remove(self)
        if len(room.sockets) == 0:
            self.session.delete()
            Rooms.all().pop(name, None)
        return self

    def room(self, name):
        room = Rooms.all().setdefault(name, Room(name))
        return Actions(room, self)

    @property
    def all(self):
        return Actions(sockets, self)


def on(route):
    def decorator(callback):
        if not routes.get(route):
            routes[route] = []

        if callback not in routes[route]:
            routes[route].append(callback)
        return callback
    return decorator


@on('connect')
def on_connect(socket):
    s = socket.session()
    socket.join('session.'+str(s.id))


@on('disconnect')
def on_disconnect(socket):
    s = socket.session()
    for name in list(socket.rooms):
        socket.leave(name)
    if s and len(socket.room('session.'+str(socket.session.id())).sockets()) == 0:
        socket.session.delete()