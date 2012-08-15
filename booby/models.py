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

        for k, v in self._fields.iteritems():
            v.validate(getattr(self, k))

    def __getitem__(self, k):
        if k not in self._fields:
            raise ValueError("Invalid field '{0}'".format(k))
        return getattr(self, k)

    def __setitem__(self, k, v):
        if k not in self._fields:
            raise ValueError("Invalid field '{0}'".format(k))
        setattr(self, k, v)

    def __iter__(self):
        return iter((x, getattr(self, x)) for x in self._fields)

    def update(self, dict_=None, **kwargs):
        if dict_ is not None:
            self._update(dict_)
        else:
            self._update(kwargs)

    def _update(self, values):
        for k, v in values.iteritems():
            self[k] = v


class Resource(Model):
    def __init__(self, **kwargs):
        super(Resource, self).__init__(**self.parse(kwargs))

    def parse(self, raw):
        return raw
