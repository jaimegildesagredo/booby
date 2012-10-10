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


from booby import fields


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['_fields'] = {}

        for base in bases:
            for k, v in base.__dict__.iteritems():
                if isinstance(v, fields.Field):
                    v.name = k
                    attrs['_fields'][k] = v

        for k, v in attrs.iteritems():
            if isinstance(v, fields.Field):
                v.name = k
                attrs['_fields'][k] = v

            if isinstance(v, ModelMeta):
                v = EmbeddedModel(v)
                attrs[k] = v
                attrs['_fields'][k] = v

        return super(ModelMeta, cls).__new__(cls, name, bases, attrs)


class Model(object):
    __metaclass__ = ModelMeta

    def __init__(self, **kwargs):
        self._data = {}

        for k, v in kwargs.iteritems():
            if k not in self._fields:
                raise ValueError("Invalid field '{0}'".format(k))
            setattr(self, k, v)

    def __getitem__(self, k):
        if k not in self._fields:
            raise ValueError("Invalid field '{0}'".format(k))
        return getattr(self, k)

    def __setitem__(self, k, v):
        if k not in self._fields:
            raise ValueError("Invalid field '{0}'".format(k))
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
        for k, v in self._fields.iteritems():
            v.validate(getattr(self, k))

    def to_dict(self):
        result = {}
        for field in self._fields:
            value = getattr(self, field)

            if isinstance(value, Model):
                result[field] = value.to_dict()
            else:
                result[field] = value
        return result


class EmbeddedModel(fields.Field):
    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner):
        if instance is not None:
            if instance._data.get(self) is None:
                instance._data[self] = self.model()
            return instance._data[self]
        return self

    def __set__(self, instance, value):
        if isinstance(value, dict):
            if instance._data.get(self) is None:
                instance._data[self] = self.model()
            instance._data[self].update(value)
        else:
            if not isinstance(value, self.model):
                raise ValueError()
            instance._data[self] = value

    def validate(self, value):
        value.validate()
