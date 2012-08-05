# -*- coding: utf-8 -*-


class Field(object):
    def __init__(self, **kwargs):
        self.name = None
        self.required = kwargs.get('required', False)

    def __get__(self, instance, owner):
        if instance is not None:
            return instance._data.get(self)
        return self

    def __set__(self, instance, value):
        if self.required and value is None:
            raise ValueError("Field '{0}' is required".format(self.name))
        instance._data[self] = value


class StringField(Field):
    pass
