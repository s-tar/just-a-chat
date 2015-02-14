#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
import imghdr
from bottle import FileUpload
from datetime import datetime
import re


class Validator:
    def __init__(self, data):
        self.data = data
        self.valid_data = data
        self.errors = {}

    def field(self, name):
        return Field(self, name)

    def fields(self, name):
        return Field(self, name, as_list=True)

    def add_error(self, field, message, code=None, index=0):
        if field not in self.errors:
            self.errors[field] = {}
        if index not in self.errors[field]:
            self.errors[field][index] = []
        self.errors[field][index].append({"code": code, "message": message})

    def get_errors(self):
        return self.errors

    def is_valid(self):
        return True if len(self.errors.keys()) == 0 else False


class Field:
    def __init__(self, validator, name, as_list=False):
        self.validator = validator
        self.name = name
        self.as_list = as_list
        if type(self.validator.data.get(self.name)) is list:
            self.val = self.validator.data.get(self.name)
        else:
            self.val = self.validator.data.getlist(self.name)


    def required(self, message=None):
        code, message = get_message("required", message)
        if len(self.val) == 0:
            self.val = ['']
        for i, val in enumerate(self.val):
            if val is None or val is "":
                self.validator.add_error(self.name, message, code, index=i)
        return self

    def integer(self, message=None, nullable=False):
        code, message = get_message("not_integer", message)
        for i, val in enumerate(self.val):
            if nullable and val is "":
                self.validator.valid_data.dict[self.name][i] = None
            else:
                try:
                    self.validator.valid_data.dict[self.name][i] = int(val)
                except ValueError:
                    self.validator.add_error(self.name, message, code, index=i)
        return self

    def boolean(self, message=None, nullable=False):
        code, message = get_message("not_boolean", message)
        for i, val in enumerate(self.val):
            if nullable and (val is "" or val is None):
                self.validator.valid_data.dict[self.name][i] = None
            elif str(val).lower() in ['none', '', 'false', '0']:
                self.validator.valid_data.dict[self.name][i] = False
            else:
                self.validator.valid_data.dict[self.name][i] = True
        return self

    def length(self, max=None, min=None, message=None):
        if max is not None and min is not None:
            for i, val in enumerate(self.val):
                val = val.decode('utf-8')
                code, message = get_message("string_not_in_range", message)
                if len(val) < min or len(val) > max:
                    self.validator.add_error(self.name, message % {'min': min, 'max': max}, code, index=i)
        elif max is not None:
            for i, val in enumerate(self.val):
                val = val.decode('utf-8')
                code, message = get_message("string_too_long", message)
                if len(val) > max:
                    self.validator.add_error(self.name, message % {'min': min, 'max': max}, code, index=i)
        elif min is not None:
            for i, val in enumerate(self.val):
                val = val.decode('utf-8')
                code, message = get_message("string_too_short", message)
                if len(val) < min:
                    self.validator.add_error(self.name, message % {'min': min, 'max': max}, code, index=i)
        return self

    def image(self, formats=['png', 'gif', 'jpg', 'jpeg', 'tiff', 'bmp'], message=None):
        for i, val in enumerate(self.val):
            if val is not None:
                code, message = get_message("not_image", message)
                filepath = val.file if type(val) is FileUpload else val
                file_type = imghdr.what(filepath)
                test_pass = False
                if type(formats) is list:
                    test_pass = file_type in formats
                else:
                    test_pass = file_type is formats
                if not test_pass:
                    self.validator.add_error(self.name, message, code, index=i)
        return self

    def email(self, message=None):
        code, message = get_message("wrong_email_format", message)
        for i, val in enumerate(self.val):
            if val is not None:
                val = val.strip()
                if re.match(r"[^@]+@[^@]+\.[^@]+", val):
                    self.validator.valid_data.dict[self.name][i] = val
                else:
                    self.validator.add_error(self.name, message, code, index=i)
        return self

    def datetime(self, message=None, format="%Y-%m-%d %H:%M:%S"):
        code, message = get_message("wrong_datetime_format", message)
        for i, val in enumerate(self.val):
            if val is not None and val != "":
                try:
                    val = val.strip()
                    self.validator.valid_data.dict[self.name][i] = datetime.strptime(val, format)
                except ValueError:
                    self.validator.add_error(self.name, message, code, index=i)
            else:
                self.validator.valid_data.dict[self.name][i] = None
        return self

def get_message(code, message):
    messages = {
        'required': "Обязательное поле",
        'not_integer': "Должно быть целым числом",
        'not_boolean': "Должно быть булевым значением",
        'string_not_in_range': "Длина текста должна быть не меньше %(min)d и не больше %(max)d символов",
        'string_too_short': 'Длина текста должна быть не меньше %(min)d символов',
        'string_too_long': 'Длина текста должна быть не больше %(max)d символов',
        'not_image': 'Файл не является картинкой',
        'wrong_email_format': 'Введен неверный адрес электронной почты',
        'wrong_datetime_format': 'Неверный формат'
    }
    if message is None:
        message = messages[code]
    return code, message




__all__ = ["Validator"]