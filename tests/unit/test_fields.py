# -*- coding: utf-8 -*-

from hamcrest import *
from nose.tools import assert_raises_regexp

from booby import Model, StringField, IntegerField, BoolField


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

    def test_invalid_value(self):
        class User(Model):
            name = StringField()

        with assert_raises_regexp(ValueError, "Invalid value for field 'name': 1"):
            User(name=1)


class TestIntegerField(object):
    def test_invalid_default_raises_value_error(self):
        with assert_raises_regexp(ValueError, 'Invalid default value: foo'):
            class User(Model):
                karma = IntegerField(default='foo')

    def test_invalid_choices_raises_value_error(self):
        with assert_raises_regexp(ValueError, "Invalid choices:"):
            class User(Model):
                karma = IntegerField(choices=['foo', 'bar'])

    def test_invalid_value_raises_value_error(self):
        class User(Model):
            karma = IntegerField()

        with assert_raises_regexp(ValueError, "Invalid value for field 'karma': foo"):
            User(karma='foo')

    def test_float(self):
        class User(Model):
            karma = IntegerField()

        assert_that(User(karma=2.7).karma, is_(2))


class TestBoolField(object):
    def test_invalid_default_raises_value_error(self):
        with assert_raises_regexp(ValueError, 'Invalid default value: foo'):
            class User(Model):
                is_active = BoolField(default='foo')

    def test_invalid_choices_raises_value_error(self):
        with assert_raises_regexp(ValueError, "Invalid choices:"):
            class User(Model):
                is_active = BoolField(choices=[True, 'foo'])

    def test_invalid_value_raises_value_error(self):
        class User(Model):
            is_active = BoolField()

        with assert_raises_regexp(ValueError, "Invalid value for field 'is_active':"):
            User(is_active='foo')

    def test_int(self):
        class User(Model):
            is_active = BoolField()

        assert_that(User(is_active=1).is_active, is_(True))
        assert_that(User(is_active=1).is_active, instance_of(bool))
