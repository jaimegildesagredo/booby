# -*- coding: utf-8 -*-

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
            raise KeyError(k)
        return getattr(self, k)

    def __setitem__(self, k, v):
        if k not in self._fields:
            raise KeyError(k)
        setattr(self, k, v)

    def __iter__(self):
        return iter((x, getattr(self, x)) for x in self._fields)
