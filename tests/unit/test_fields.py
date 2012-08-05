# -*- coding: utf-8 -*-

from hamcrest import *
from nose.tools import assert_raises_regexp

from booby import Model, StringField


class TestField(object):
    def test_required(self):
        class User(Model):
            name = StringField(required=True)

        with assert_raises_regexp(ValueError, "Field 'name' is required"):
            User(name=None)

    def test_required_default_is_false(self):
        class User(Model):
            name = StringField()

        user = User(name=None)

        assert_that(user.name, is_(None))
