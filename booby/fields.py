# -*- coding: utf-8 -*-


class Field(object):
    def __get__(self, instance, owner):
        if instance is not None:
            return None
        return self


class StringField(Field):
    pass
