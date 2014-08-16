# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from expects import *
from .._helpers import Spy, stub_validator

from booby import fields, errors, models

IRRELEVANT_VALUE = 'irrelevant value'
NUMERIC_STRING_VALUE = '137'


class TestOptions(object):
    def test_should_be_passed_kwargs_dict(self):
        kwargs = dict(required=True, primary=True, foo='bar')

        field = fields.Field(**kwargs)

        expect(field.options).to(equal(kwargs))

    def test_should_be_empty_dict_if_no_kwargs_passed(self):
        field = fields.Field()

        expect(field.options).to(equal({}))


class TestFieldDefault(object):
    def test_when_access_obj_field_and_value_is_not_assigned_yet_then_is_default(self):
        user = User()

        expect(user.name).to(equal('nobody'))

    def test_when_default_is_callable_then_use_its_returned_value_as_field_default(self):
        default = 'anonymous'
        User.name.default = lambda: default

        user = User()

        expect(user.name).to(be(default))

    def test_when_callable_receives_argument_then_pass_owner_instance(self):
        User.name.default = lambda model: model == user

        user = User()

        expect(user.name).to(be_true)

    def test_when_callable_raises_type_error_then_should_not_be_catched(self):
        def callback():
            raise TypeError('foo')

        User.name.default = callback

        expect(lambda: User().name).to(raise_error(TypeError, 'foo'))

    def test_when_default_is_callable_then_should_be_called_once_per_onwer_instance(self):
        default_callable = Spy()

        User.name.default = default_callable

        user = User()
        user.name
        user.name

        expect(default_callable.times_called).to(equal(1))

    def test_when_default_is_callable_then_should_be_called_on_each_owner_instance(self):
        default_callable = Spy()
        User.name.default = default_callable

        User().name
        User().name

        expect(default_callable.times_called).to(equal(2))


class TestFieldValues(object):
    def test_when_access_obj_field_and_value_is_already_assigned_then_is_value(self):
        user = User()
        user.name = 'Jack'

        expect(user.name).to(equal('Jack'))

    def test_when_access_class_field_then_is_field_object(self):
        expect(User.name).to(be_a(fields.Field))


class TestValidateField(object):
    def test_when_validate_without_validation_errors_then_does_not_raise(self):
        field = fields.Field(stub_validator, stub_validator)

        field.validate('foo')

    def test_when_first_validator_raises_validation_error_then_raises_exception(self):
        def validator1(value):
            if value == 'foo':
                raise errors.ValidationError()

        field = fields.Field(validator1, stub_validator)

        expect(lambda: field.validate('foo')).to(raise_error(
            errors.ValidationError))

    def test_when_second_validator_raises_validation_error_then_raises_exception(self):
        def validator2(value):
            if value == 'foo':
                raise errors.ValidationError()

        field = fields.Field(stub_validator, validator2)

        expect(lambda: field.validate('foo')).to(raise_error(
            errors.ValidationError))


class TestFieldBuiltinValidations(object):
    def test_when_required_is_true_then_value_shouldnt_be_none(self):
        field = fields.Field(required=True)

        expect(lambda: field.validate(None)).to(raise_error(
            errors.ValidationError, end_with('required')))

    def test_when_required_is_false_then_value_can_be_none(self):
        field = fields.Field(required=False)

        field.validate(None)

    def test_when_not_required_then_value_can_be_none(self):
        field = fields.Field()

        field.validate(None)

    def test_when_choices_then_value_should_be_in_choices(self):
        field = fields.Field(choices=['foo', 'bar'])

        expect(lambda: field.validate('baz')).to(raise_error(
            errors.ValidationError, contain(' in ')))

    def test_when_not_choices_then_value_can_be_whatever_value(self):
        field = fields.Field()

        field.validate('foo')


class TestEncode(object):
    def test_should_return_value_if_there_are_not_encoders(self):
        field = fields.Field()

        expect(field.encode(IRRELEVANT_VALUE)).to(equal(IRRELEVANT_VALUE))

    def test_should_return_value_returned_by_encoder(self):
        def encoder(value):
            return value.swapcase()

        field = fields.Field(encoders=[encoder])

        expect(field.encode(IRRELEVANT_VALUE)).to(equal(
            IRRELEVANT_VALUE.swapcase()))

    def test_should_return_value_returned_by_encoders_in_order(self):
        def encoder1(value):
            return int(value)

        def encoder2(value):
            return str(value)

        field = fields.Field(encoders=[encoder1, encoder2])

        expect(field.encode(NUMERIC_STRING_VALUE)).to(equal(
            NUMERIC_STRING_VALUE))


class TestDecode(object):
    def test_should_return_value_if_there_are_not_decoders(self):
        field = fields.Field()

        expect(field.decode(IRRELEVANT_VALUE)).to(equal(IRRELEVANT_VALUE))

    def test_should_return_value_returned_by_decoder(self):
        def decoder(value):
            return value.swapcase()

        field = fields.Field(decoders=[decoder])

        expect(field.decode(IRRELEVANT_VALUE)).to(equal(
            IRRELEVANT_VALUE.swapcase()))

    def test_should_return_value_returned_by_decoders_in_order(self):
        def decoder1(value):
            return int(value)

        def decoder2(value):
            return str(value)

        field = fields.Field(decoders=[decoder1, decoder2])

        expect(field.decode(NUMERIC_STRING_VALUE)).to(equal(NUMERIC_STRING_VALUE))


class User(models.Model):
    name = fields.String(default='nobody')
    email = fields.String()
