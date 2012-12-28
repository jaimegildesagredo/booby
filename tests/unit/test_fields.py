# -*- coding: utf-8 -*-

from hamcrest import *
from doublex import Stub
from nose.tools import assert_raises, assert_raises_regexp

from booby import fields, errors, models


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


class TestEmbeddedFieldDescriptor(object):
    def test_when_set_field_value_with_dict_then_value_is_embedded_object_with_dict_values(self):
        self.group.admin = {'name': u'foo', 'email': u'foo@example.com'}

        assert_that(self.group.admin, instance_of(User))
        assert_that(self.group.admin.name, is_(u'foo'))
        assert_that(self.group.admin.email, is_(u'foo@example.com'))

    def test_when_set_field_value_with_dict_with_invalid_field_then_raises_field_error(self):
        with assert_raises_regexp(errors.FieldError, 'foo'):
            self.group.admin = {'name': u'foo', 'foo': u'bar'}

    def test_when_set_field_value_with_not_dict_object_then_value_is_given_object(self):
        user = User(name=u'foo', email=u'foo@example.com')
        self.group.admin = user

        assert_that(self.group.admin, is_(user))

    def test_when_set_field_with_not_model_instance_then_value_is_given_object(self):
        user = object()
        self.group.admin = user

        assert_that(self.group.admin, is_(user))

    def setup(self):
        self.group = Group()


class User(models.Model):
    name = fields.StringField(default='nobody')
    email = fields.StringField()


class Group(models.Model):
    name = fields.StringField()
    admin = fields.EmbeddedField(User)


class TestValidateField(object):
    def test_when_validate_without_validation_errors_then_does_not_raise(self):
        validator1 = Stub()
        validator2 = Stub()

        field = fields.Field(validator1, validator2)

        field.validate('foo')

    def test_when_first_validator_raises_validation_error_then_raises_exception(self):
        with Stub() as validator1:
            validator1.validate('foo').raises(errors.ValidationError)

        validator2 = Stub()

        field = fields.Field(validator1, validator2)

        with assert_raises(errors.ValidationError):
            field.validate('foo')

    def test_when_second_validator_raises_validation_error_then_raises_exception(self):
        validator1 = Stub()

        with Stub() as validator2:
            validator2.validate('foo').raises(errors.ValidationError)

        field = fields.Field(validator1, validator2)

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


class TestEmbeddedFieldBuildtinValidators(object):
    def test_when_value_is_not_instance_of_model_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'instance of'):
            self.field.validate(object())

    def test_when_embedded_model_field_has_invalid_value_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'string'):
            self.field.validate(User(name=1))

    def test_when_embedded_model_validates_then_does_not_raise(self):
        self.field.validate(User())

    def setup(self):
        self.field = fields.EmbeddedField(User)
