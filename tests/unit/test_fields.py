# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from expects import expect
from ._helpers import Spy, stub_validator

from booby import fields, errors, models


class TestFieldInit(object):
    def test_when_kwargs_then_field_options_is_a_dict_with_these_args(self):
        kwargs = dict(required=True, primary=True, foo='bar')

        field = fields.Field(**kwargs)

        expect(field.options).to.equal(kwargs)

    def test_when_no_kwargs_then_field_options_is_an_empty_dict(self):
        field = fields.Field()

        expect(field.options).to.equal({})


class TestFieldDefault(object):
    def test_when_access_obj_field_and_value_is_not_assigned_yet_then_is_default(self):
        user = User()

        expect(user.name).to.equal('nobody')

    def test_when_default_is_callable_then_use_its_returned_value_as_field_default(self):
        default = 'anonymous'
        User.name.default = lambda: default

        user = User()

        expect(user.name).to.be(default)

    def test_when_callable_receives_argument_then_pass_owner_instance(self):
        User.name.default = lambda model: model

        user = User()

        expect(user.name).to.be(user)

    def test_when_callable_raises_type_error_then_should_not_be_catched(self):
        def callback():
            raise TypeError('foo')

        User.name.default = callback

        expect(lambda: User().name).to.raise_error(TypeError, 'foo')

    def test_when_default_is_callable_then_should_be_called_once_per_onwer_instance(self):
        default_callable = Spy()

        User.name.default = default_callable

        user = User()
        user.name
        user.name

        expect(default_callable.times_called).to.equal(1)

    def test_when_default_is_callable_then_should_be_called_on_each_owner_instance(self):
        default_callable = Spy()
        User.name.default = default_callable

        User().name
        User().name

        expect(default_callable.times_called).to.equal(2)


class TestFieldValues(object):
    def test_when_access_obj_field_and_value_is_already_assigned_then_is_value(self):
        user = User()
        user.name = 'Jack'

        expect(user.name).to.equal('Jack')

    def test_when_access_class_field_then_is_field_object(self):
        expect(User.name).to.be.a(fields.Field)


class TestEmbeddedFieldDescriptor(object):
    def test_when_set_field_value_with_dict_then_value_is_embedded_object_with_dict_values(self):
        self.group.admin = {'name': 'foo', 'email': 'foo@example.com'}

        expect(self.group.admin).to.be.an(User)
        expect(self.group.admin).to.have.properties(
            name='foo', email='foo@example.com')

    def test_when_set_field_value_with_dict_with_invalid_field_then_raises_field_error(self):
        def callback():
            self.group.admin = {'name': 'foo', 'foo': 'bar'}

        expect(callback).to.raise_error(errors.FieldError, 'foo')

    def test_when_set_field_value_with_not_dict_object_then_value_is_given_object(self):
        user = User(name='foo', email='foo@example.com')
        self.group.admin = user

        expect(self.group.admin).to.be(user)

    def test_when_set_field_with_not_model_instance_then_value_is_given_object(self):
        user = object()
        self.group.admin = user

        expect(self.group.admin).to.be(user)

    def setup(self):
        self.group = Group()


class User(models.Model):
    name = fields.String(default='nobody')
    email = fields.String()


class Group(models.Model):
    name = fields.String()
    admin = fields.Embedded(User)


class TestValidateField(object):
    def test_when_validate_without_validation_errors_then_does_not_raise(self):
        field = fields.Field(stub_validator, stub_validator)

        field.validate('foo')

    def test_when_first_validator_raises_validation_error_then_raises_exception(self):
        def validator1(value):
            if value == 'foo':
                raise errors.ValidationError()

        field = fields.Field(validator1, stub_validator)

        expect(lambda: field.validate('foo')).to.raise_error(
            errors.ValidationError)

    def test_when_second_validator_raises_validation_error_then_raises_exception(self):
        def validator2(value):
            if value == 'foo':
                raise errors.ValidationError()

        field = fields.Field(stub_validator, validator2)

        expect(lambda: field.validate('foo')).to.raise_error(
            errors.ValidationError)


class TestFieldBuiltinValidations(object):
    def test_when_required_is_true_then_value_shouldnt_be_none(self):
        field = fields.Field(required=True)

        expect(lambda: field.validate(None)).to.raise_error(
            errors.ValidationError, 'required')

    def test_when_required_is_false_then_value_can_be_none(self):
        field = fields.Field(required=False)

        field.validate(None)

    def test_when_not_required_then_value_can_be_none(self):
        field = fields.Field()

        field.validate(None)

    def test_when_choices_then_value_should_be_in_choices(self):
        field = fields.Field(choices=['foo', 'bar'])

        expect(lambda: field.validate('baz')).to.raise_error(
            errors.ValidationError, ' in ')

    def test_when_not_choices_then_value_can_be_whatever_value(self):
        field = fields.Field()

        field.validate('foo')


class TestEmbeddedFieldBuildtinValidators(object):
    def test_when_value_is_not_instance_of_model_then_raises_validation_error(self):
        expect(lambda: self.field.validate(object())).to.raise_error(
            errors.ValidationError, 'instance of')

    def test_when_embedded_model_field_has_invalid_value_then_raises_validation_error(self):
        expect(lambda: self.field.validate(User(name=1))).to.raise_error(
            errors.ValidationError, 'string')

    def test_when_embedded_model_validates_then_does_not_raise(self):
        self.field.validate(User())

    def setup(self):
        self.field = fields.Embedded(User)
