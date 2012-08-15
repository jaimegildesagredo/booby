# -*- coding: utf-8 -*-

from hamcrest import *
from nose.tools import assert_raises_regexp

from booby import Model, Resource, StringField


class TestResource(object):
    def test_is_model_subclass(self):
        assert_that(issubclass(Resource, Model))

    def test_init_with_custom_parse_method(self):
        class UserWithCustomParseMethod(User):
            def parse(self, raw):
                return {
                    'name': raw['name'],
                    'email': raw['email']}

        user = UserWithCustomParseMethod(
            name=u'foo', email=u'foo@example.com', valid=u'foo')

        assert_that(user.name, is_(u'foo'))
        assert_that(user.email, is_(u'foo@example.com'))

    def test_init_with_default_parse_method(self):
        user = User(name=u'foo', email=u'foo@example.com')

        assert_that(user.name, is_(u'foo'))
        assert_that(user.email, is_(u'foo@example.com'))

    def test_init_with_default_parse_method_and_invalid_field_raises_value_error(self):
        with assert_raises_regexp(ValueError, "Invalid field 'invalid'"):
            User(name=u'foo', email=u'foo@example.com', invalid=u'foo')


class TestDictResource(object):
    def test_update_with_custom_parse_method(self):
        class UserWithCustomParseMethod(User):
            def parse(self, raw):
                return {
                    'name': raw['name'],
                    'email': raw['email']}

        user = UserWithCustomParseMethod(name=u'foo', email='roo@example.com')
        user.update({'name': u'foobar', 'email': u'foo@bar.com', 'invalid': u'foo'})

        assert_that(user.name, is_(u'foobar'))
        assert_that(user.email, is_(u'foo@bar.com'))


class User(Resource):
    name = StringField()
    email = StringField()
