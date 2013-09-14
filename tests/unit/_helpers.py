# -*- coding: utf-8 -*-


def stub_validator(value):
    pass


class Spy(object):
    def __init__(self):
        self.times_called = 0

    def __call__(self):
        self.times_called += 1
