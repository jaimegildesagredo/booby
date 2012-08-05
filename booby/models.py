# -*- coding: utf-8 -*-


class Model(object):
    def __init__(self, **kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def __iter__(self):
        return iter((x, getattr(self, x)) for x in self.__dict__)
