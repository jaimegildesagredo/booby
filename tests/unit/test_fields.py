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

    def test_default(self):
        class User(Model):
            name = StringField(default='anonymous')

        assert_that(User().name, is_('anonymous'))


class TestFieldChoices(object):
    def test_empty_list(self):
        class User(Model):
            name = StringField(choices=[])

        assert_that(User(name='foo').name, is_('foo'))

    def test_not_in_choices_raises_value_error(self):
        class User(Model):
            name = StringField(choices=['foo', 'bar'])

        with assert_raises_regexp(ValueError, "Invalid value for field 'name': foobar"):
            User(name='foobar')

    def test_not_sequence_raises_value_error(self):
        with assert_raises_regexp(TypeError, "'choices' is not iterable"):
            class User(Model):
                name = StringField(choices=object())


class TestStringField(object):
    def test_invalid_default_raises_value_error(self):
        with assert_raises_regexp(ValueError, 'Invalid default value: 1'):
            class User(Model):
                name = StringField(default=1)

    def test_invalid_choices_raises_value_error(self):
        with assert_raises_regexp(ValueError, "Invalid choices:"):
            class User(Model):
                name = StringField(choices=[1, 'foo'])
