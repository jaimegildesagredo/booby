# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json

from hamcrest import *
from nose.tools import assert_raises_regexp

from booby import errors, fields, models


class TestDefaultModelInit(object):
    def test_when_pass_kwargs_then_set_fields_values(self):
        user = User(name='foo', email='foo@example.com')

        assert_that(user.name, is_('foo'))
        assert_that(user.email, is_('foo@example.com'))

    def test_when_pass_kwargs_without_required_field_then_required_field_is_none(self):
        user = UserWithRequiredName(email='foo@example.com')

        assert_that(user.name, is_(None))

    def test_when_pass_invalid_field_in_kwargs_then_raises_field_error(self):
        with assert_raises_regexp(errors.FieldError, "'User' model has no field 'foo'"):
            User(foo='bar')


class TestOverridenModelInit(object):
    def test_when_pass_args_then_set_fields_values(self):
        class UserWithOverridenInit(User):
            def __init__(self, name, email):
                self.name = name
                self.email = email

        user = UserWithOverridenInit('foo', 'foo@example.com')

        assert_that(user.name, is_('foo'))
        assert_that(user.email, is_('foo@example.com'))


class TestModelData(object):
    def test_when_set_field_value_then_another_model_shouldnt_have_the_same_value(self):
        user = User(name='foo')
        another = User(name='bar')

        assert_that(user.name, is_not(another.name))

    # TODO: Is this an itegration test?
    def test_when_validate_without_required_fields_then_raises_validation_error(self):
        user = UserWithRequiredName(email='foo@example.com')

        with assert_raises_regexp(errors.ValidationError, 'required'):
            user.validate()


class TestInheritedModel(object):
    def test_when_pass_kwargs_then_set_fields_values(self):
        user = UserWithPage(name='foo', email='foo@example.com', page='example.com')

        assert_that(user.name, is_('foo'))
        assert_that(user.email, is_('foo@example.com'))
        assert_that(user.page, is_('example.com'))

    def test_when_pass_invalid_field_in_kwargs_then_raises_field_error(self):
        with assert_raises_regexp(errors.FieldError, "'UserWithPage' model has no field 'foo'"):
            UserWithPage(foo='bar')

    def test_when_override_superclass_field_then_validates_subclass_field(self):
        class UserWithoutRequiredName(UserWithRequiredName):
            name = fields.StringField()

        user = UserWithoutRequiredName()
        user.validate()


class TestInheritedMixin(object):
    def test_when_pass_kwargs_then_set_fields_values(self):
        user = UserWithEmail(name='foo', email='foo@example.com')

        assert_that(user.name, is_('foo'))
        assert_that(user.email, is_('foo@example.com'))

    def test_when_pass_invalid_field_in_kwargs_then_raises_field_error(self):
        with assert_raises_regexp(errors.FieldError, "'UserWithEmail' model has no field 'foo'"):
            UserWithEmail(foo='bar')

    def test_when_override_mixin_field_then_validates_subclass_field(self):
        class User(UserMixin, models.Model):
            name = fields.StringField(required=True)

        user = User()

        with assert_raises_regexp(errors.ValidationError, 'required'):
            user.validate()


class TestDictModel(object):
    def test_when_get_field_then_returns_value(self):
        assert_that(self.user['name'], is_('foo'))

    def test_when_get_invalid_field_then_raises_field_error(self):
        with assert_raises_regexp(errors.FieldError, "'User' model has no field 'foo'"):
            self.user['foo']

    def test_when_set_field_then_update_field_value(self):
        self.user['name'] = 'bar'

        assert_that(self.user.name, is_('bar'))

    def test_when_set_invalid_field_then_raises_field_error(self):
        with assert_raises_regexp(errors.FieldError, "'User' model has no field 'foo'"):
            self.user['foo'] = 'bar'

    def test_when_update_with_dict_then_update_fields_values(self):
        self.user.update({'name': 'foobar', 'email': 'foo@bar.com'})

        assert_that(self.user.name, is_('foobar'))
        assert_that(self.user.email, is_('foo@bar.com'))

    def test_when_update_kw_arguments_then_update_fields_values(self):
        self.user.update(name='foobar', email='foo@bar.com')

        assert_that(self.user.name, is_('foobar'))
        assert_that(self.user.email, is_('foo@bar.com'))

    def test_when_update_invalid_field_then_raises_field_error(self):
        with assert_raises_regexp(errors.FieldError, "'User' model has no field 'foo'"):
            self.user.update(foo='bar')

    def setup(self):
        self.user = User(name='foo', email='roo@example.com')


class TestModelToDict(object):
    def test_when_model_has_single_fields_then_returns_dict_with_fields_values(self):
        user = User(name='foo', email='roo@example.com')

        assert_that(user.to_dict(), has_entries(
            name='foo',
            email='roo@example.com'
        ))

    def test_when_model_has_embedded_model_field_then_returns_dict_with_inner_dict(self):
        class Token(models.Model):
            key = fields.StringField()
            secret = fields.StringField()

        class UserWithToken(User):
            token = fields.Field()

        token = Token(key='foo', secret='bar')
        user = UserWithToken(name='foo', email='roo@example.com', token=token)

        assert_that(user.to_dict(), has_entries(
            name='foo',
            email='roo@example.com',
            token=has_entries(
                key='foo',
                secret='bar'
            )
        ))


class TestModelToJSON(object):
    def test_when_model_has_single_fields_then_returns_json_with_fields_values(self):
        user = User(name='Jack', email='jack@example.com')

        assert_that(user.to_json(), is_(json.dumps(user.to_dict())))


class User(models.Model):
    name = fields.StringField()
    email = fields.StringField()


class UserWithRequiredName(User):
    name = fields.StringField(required=True)


class UserWithPage(User):
    page = fields.StringField()


class UserMixin(object):
    name = fields.StringField()


class UserWithEmail(UserMixin, models.Model):
    email = fields.StringField()
