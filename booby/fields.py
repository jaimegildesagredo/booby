# -*- coding: utf-8 -*-


class Field(object):
    def __init__(self, **kwargs):
        self.name = None
        self.required = kwargs.get('required', False)

        default = kwargs.get('default')
        self.default = self.validate(default) if default is not None else default

    def __get__(self, instance, owner):
        if instance is not None:
            return instance._data.get(self, self.default)
        return self

    def __set__(self, instance, value):
        if self.required and value is None:
            raise ValueError("Field '{0}' is required".format(self.name))
        instance._data[self] = value

    def validate(self, value):
        raise NotImplementedError()


class StringField(Field):
    def validate(self, value):
        if not isinstance(value, basestring):
            raise ValueError('Invalid value: {0}'.format(value))
        return value
