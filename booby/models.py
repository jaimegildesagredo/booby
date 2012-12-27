# -*- coding: utf-8 -*-
#
# Copyright 2012 Jaime Gil de Sagredo Luna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from booby import fields, errors


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['_fields'] = {}

        for base in bases:
            for k, v in base.__dict__.iteritems():
                if isinstance(v, fields.Field):
                    attrs['_fields'][k] = v

        for k, v in attrs.iteritems():
            if isinstance(v, fields.Field):
                attrs['_fields'][k] = v

        return super(ModelMeta, cls).__new__(cls, name, bases, attrs)


class Model(object):
    __metaclass__ = ModelMeta

    def __new__(cls, *args, **kwargs):
        model = super(Model, cls).__new__(cls)
        model._data = {}

        return model

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if k not in self._fields:
                self.__raise_field_error(k)

            setattr(self, k, v)

    def __raise_field_error(self, name):
        raise errors.FieldError("'{}' model has no field '{}'".format(
            type(self).__name__, name))

    def __getitem__(self, k):
        if k not in self._fields:
            self.__raise_field_error(k)

        return getattr(self, k)

    def __setitem__(self, k, v):
        if k not in self._fields:
            self.__raise_field_error(k)

        setattr(self, k, v)

    def update(self, dict_=None, **kwargs):
        if dict_ is not None:
            self._update(dict_)
        else:
            self._update(kwargs)

    def _update(self, values):
        for k, v in values.iteritems():
            self[k] = v

    def validate(self):
        for name, field in self._fields.iteritems():
            field.validate(getattr(self, name))

    def to_dict(self):
        result = {}
        for field in self._fields:
            value = getattr(self, field)

            if isinstance(value, Model):
                result[field] = value.to_dict()
            else:
                result[field] = value
        return result

    def to_json(self):
        return json.dumps(self.to_dict())
