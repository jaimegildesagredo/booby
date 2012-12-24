# -*- coding: utf-8 -*-

from hamcrest import *
from doublex import Stub
from nose.tools import assert_raises, assert_raises_regexp

from booby import fields, errors
from booby.models import Model


class TestFieldDescriptor(object):
    def test_when_access_obj_field_and_value_is_not_assigned_yet_then_is_default(self):
        user = User()

        assert_that(user.name, is_('nobody'))

    def test_when_access_obj_field_and_value_is_already_assigned_then_is_value(self):
        user = User()
        user.name = 'Jack'

        assert_that(user.name, is_('Jack'))

    def test_when_access_class_field_then_is_field_object(self):
        assert_that(User.name, instance_of(fields.Field))


class User(Model):
    name = fields.Field(default='nobody')


class TestValidateField(object):
    def test_when_validate_without_validation_errors_then_does_not_raise(self):
        validator1 = Stub()
        validator2 = Stub()

        field = fields.Field(validators=[validator1, validator2])

        field.validate('foo')

    def test_when_validate_with_validation_error_then_raises_exception(self):
        validator1 = Stub()

        with Stub() as validator2:
            validator2.validate('foo').raises(errors.ValidationError)

        field = fields.Field(validators=[validator1, validator2])

        with assert_raises(errors.ValidationError):
            field.validate('foo')


class TestFieldBuiltinValidations(object):
    def test_when_required_is_true_then_value_shouldnt_be_none(self):
        field = fields.Field(required=True)

        with assert_raises_regexp(errors.ValidationError, 'required'):
            field.validate(None)

    def test_when_required_is_false_then_value_can_be_none(self):
        field = fields.Field(required=False)

        field.validate(None)

    def test_when_not_required_then_value_can_be_none(self):
        field = fields.Field()

        field.validate(None)

    def test_when_choices_then_value_should_be_in_choices(self):
        field = fields.Field(choices=['foo', 'bar'])

        with assert_raises_regexp(errors.ValidationError, ' in '):
            field.validate('baz')

    def test_when_not_choices_then_value_can_be_whatever_value(self):
        field = fields.Field()

        field.validate('foo')
