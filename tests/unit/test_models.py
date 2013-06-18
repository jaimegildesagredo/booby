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


class TestValidateModel(object):
    def test_when_validate_and_validation_errors_then_raises_first_validation_error(self):
        user = UserWithRequiredName(email='foo@example.com')

        with assert_raises_regexp(errors.ValidationError, 'required'):
            user.validate()

    def test_when_validate_without_errors_then_does_not_raise(self):
        user = UserWithRequiredName(name='Jack')

        user.validate()

    def test_when_validation_errors_and_errors_then_returns_dict_of_name_and_errors(self):
        user = UserWithRequiredFields(id=1, role='root')

        errors = user.validation_errors()

        assert_that(errors, has_entries(
            id=matches_regexp('be a string'),
            role=matches_regexp('be in'),
            name=matches_regexp('required')))

    def test_when_validation_errors_and_no_errors_then_returns_none(self):
        user = UserWithRequiredName(name='jack')

        errors = user.validation_errors()

        assert_that(errors, is_(None))


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
        class UserWithToken(User):
            token = fields.Field()

        user = UserWithToken(name='foo', email='roo@example.com', token=self.token1)

        assert_that(user.to_dict(), has_entries(
            name='foo',
            email='roo@example.com',
            token=has_entries(self.token1.to_dict())))

    def test_when_model_has_list_of_models_then_returns_list_of_dicts(self):
        user = UserWithList(tokens=[self.token1, self.token2])

        assert_that(user.to_dict(), has_entry('tokens', [
            self.token1.to_dict(), self.token2.to_dict()]))

    def test_when_model_has_list_of_models_and_values_then_returns_list_of_dicts_and_values(self):
        user = UserWithList(tokens=[self.token1, 'foo', self.token2])

        assert_that(user.to_dict(), has_entry('tokens', [
            self.token1.to_dict(), 'foo', self.token2.to_dict()]))

    def setup(self):
        self.token1 = Token(key='foo', secret='bar')
        self.token2 = Token(key='fuu', secret='baz')


class TestModelToJSON(object):
    def test_when_model_has_single_fields_then_returns_json_with_fields_values(self):
        result = self.user.to_json()

        assert_that(result, is_(json.dumps(self.user.to_dict())))

    def test_when_pass_extra_arguments_then_call_json_dump_function_with_these_args(self):
        result = self.user.to_json(indent=2)

        assert_that(result, is_(json.dumps(self.user.to_dict(), indent=2)))

    def setup(self):
        self.user = User(name='Jack', email='jack@example.com')


class User(models.Model):
    name = fields.StringField()
    email = fields.StringField()


class UserWithRequiredName(User):
    name = fields.StringField(required=True)


class UserWithRequiredFields(UserWithRequiredName):
    id = fields.StringField()
    role = fields.StringField(choices=['admin', 'user'])


class UserWithPage(User):
    page = fields.StringField()


class UserMixin(object):
    name = fields.StringField()


class UserWithEmail(UserMixin, models.Model):
    email = fields.StringField()


class UserWithList(User):
    tokens = fields.Field()


class Token(models.Model):
    key = fields.StringField()
    secret = fields.StringField()
