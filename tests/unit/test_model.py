# -*- coding: utf-8 -*-

import json

from hamcrest import *
from nose.tools import assert_raises_regexp

from booby import errors, fields, Model


class TestDefaultModelInit(object):
    def test_when_pass_kwargs_then_set_fields_values(self):
        user = User(name=u'foo', email=u'foo@example.com')

        assert_that(user.name, is_(u'foo'))
        assert_that(user.email, is_(u'foo@example.com'))

    def test_when_pass_kwargs_without_required_field_then_required_field_is_none(self):
        user = UserWithRequiredName(email='foo@example.com')

        assert_that(user.name, is_(None))

    def test_when_pass_invalid_field_in_kwargs_then_raises_field_error(self):
        with assert_raises_regexp(errors.FieldError, "'User' model has no field 'foo'"):
            User(foo=u'bar')


class TestOverridenModelInit(object):
    def test_when_pass_args_then_set_fields_values(self):
        class UserWithOverridenInit(User):
            def __init__(self, name, email):
                self.name = name
                self.email = email

        user = UserWithOverridenInit(u'foo', u'foo@example.com')

        assert_that(user.name, is_(u'foo'))
        assert_that(user.email, is_(u'foo@example.com'))


class TestModelDeclaration(object):
    pass


class TestInheritedModelDeclaration(object):
    # TODO: This test case should be the same tests for models but using an inherited model
    def test_when_override_superclass_field_then_superclass_and_subclass_does_not_share_the_same_field(self):
        class UserWithPage(User):
            name = fields.StringField()
            page = fields.StringField()

        assert_that(UserWithPage.name, is_not(User.name))


class TestInheritedMixinDeclaration(object):
    # TODO: This test case should be the same tests for models but using an inherited mixin
    def test_when_override_superclass_field_then_superclass_and_subclass_does_not_share_the_same_field(self):
        class UserWithEmail(UserMixin, Model):
            name = fields.StringField()
            email = fields.StringField()

        assert_that(UserWithEmail.name, is_not(UserMixin.name))


class TestModelData(object):
    def test_when_set_field_value_then_another_model_shouldnt_have_the_same_value(self):
        user = User(name=u'foo')
        another = User(name=u'bar')

        assert_that(user.name, is_not(another.name))

    # TODO: Is this an itegration test?
    def test_when_validate_without_required_fields_then_raises_validation_error(self):
        user = UserWithRequiredName(email='foo@example.com')

        with assert_raises_regexp(errors.ValidationError, 'required'):
            user.validate()


class TestDictModel(object):
    def test_get_field_value(self):
        assert_that(self.user['name'], is_(u'foo'))

    def test_get_invalid_field_raises_key_error(self):
        with assert_raises_regexp(ValueError, "Invalid field 'invalid'"):
            self.user['invalid']

    def test_set_field_value(self):
        self.user['name'] = u'bar'

        assert_that(self.user['name'], is_(u'bar'))

    def test_set_invalid_field_raises_key_error(self):
        with assert_raises_regexp(ValueError, "Invalid field 'invalid'"):
            self.user['invalid'] = u'foo'

    def test_update_updates_fields(self):
        self.user.update({'name': u'foobar', 'email': u'foo@bar.com'})

        assert_that(self.user.name, is_(u'foobar'))
        assert_that(self.user.email, is_(u'foo@bar.com'))

    def test_update_kw_fields_updates_fields(self):
        self.user.update(name=u'foobar', email=u'foo@bar.com')

        assert_that(self.user.name, is_(u'foobar'))
        assert_that(self.user.email, is_(u'foo@bar.com'))

    def test_update_invalid_field_raises_value_error(self):
        with assert_raises_regexp(ValueError, "Invalid field 'invalid'"):
            self.user.update(invalid=u'foo')

    def setup(self):
        self.user = User(name=u'foo', email='roo@example.com')


class TestModelToDict(object):
    def test_when_model_has_single_fields_then_returns_dict_with_fields_values(self):
        user = User(name=u'foo', email='roo@example.com')

        assert_that(user.to_dict(), has_entries(
            name=u'foo',
            email='roo@example.com'
        ))

    def test_when_model_has_embedded_model_field_then_returns_dict_with_inner_dict(self):
        class Token(Model):
            key = fields.StringField()
            secret = fields.StringField()

        class UserWithToken(User):
            token = fields.Field()

        token = Token(key=u'foo', secret=u'bar')
        user = UserWithToken(name=u'foo', email=u'roo@example.com', token=token)

        assert_that(user.to_dict(), has_entries(
            name=u'foo',
            email=u'roo@example.com',
            token=has_entries(
                key=u'foo',
                secret=u'bar'
            )
        ))


class TestModelToJSON(object):
    def test_when_model_has_single_fields_then_returns_json_with_fields_values(self):
        user = User(name=u'Jack', email=u'jack@example.com')

        assert_that(user.to_json(), is_(json.dumps(user.to_dict())))


class User(Model):
    name = fields.StringField()
    email = fields.StringField()


class UserMixin(object):
    name = fields.StringField()


class UserWithRequiredName(User):
    name = fields.StringField(required=True)
