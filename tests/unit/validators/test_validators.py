# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from expects import expect
from . import mixins
from .._helpers import stub_validator

from booby import validators, fields, models, errors


class TestRequired(object):
    def test_when_value_is_none_then_raises_validation_error(self):
        expect(lambda: self.validator(None)).to.raise_error(
            errors.ValidationError, 'is required')

    def test_when_value_is_not_none_then_does_not_raise(self):
        self.validator('foo')

    def setup(self):
        self.validator = validators.Required()


class TestIn(object):
    def test_when_value_is_not_in_choices_then_raises_validation_error(self):
        expect(lambda: self.validator('baz')).to.raise_error(
            errors.ValidationError, "should be in \[u?'foo', u?'bar'\]")

    def test_when_value_is_in_choices_then_does_not_raise(self):
        self.validator('bar')

    def setup(self):
        self.validator = validators.In(['foo', 'bar'])


class TestString(mixins.String):
    def test_when_value_is_a_string_then_does_not_raise(self):
        self.validator('foo')

    def test_when_value_is_unicode_then_does_not_raise(self):
        self.validator('foo')

    def setup(self):
        self.validator = validators.String()


class TestInteger(object):
    def test_when_value_is_not_an_integer_then_raises_validation_error(self):
        expect(lambda: self.validator('foo')).to.raise_error(
            errors.ValidationError, 'should be an integer')

    def test_when_value_is_an_integer_then_does_not_raise(self):
        self.validator(1)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator(None)

    def setup(self):
        self.validator = validators.Integer()


class TestFloat(object):
    def test_when_value_is_not_a_float_then_raises_validation_error(self):
        expect(lambda: self.validator('foo')).to.raise_error(
            errors.ValidationError, 'should be a float')

    def test_when_value_is_a_float_then_does_not_raise(self):
        self.validator(1.0)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator(None)

    def setup(self):
        self.validator = validators.Float()


class TestBoolean(object):
    def test_when_value_is_not_a_boolean_then_raises_validation_error(self):
        expect(lambda: self.validator('foo')).to.raise_error(
            errors.ValidationError, 'should be a boolean')

    def test_when_value_is_a_boolean_then_does_not_raises(self):
        self.validator(False)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator(None)

    def setup(self):
        self.validator = validators.Boolean()


class TestModel(object):
    def test_when_value_is_not_instance_of_model_then_raises_validation_error(self):
        expect(lambda: self.validator(object())).to.raise_error(
            errors.ValidationError, "should be an instance of 'User'")

    def test_when_model_validate_raises_validation_error_then_raises_validation_error(self):
        class InvalidUser(User):
            def validate(self):
                raise errors.ValidationError()

        expect(lambda: self.validator(InvalidUser())).to.raise_error(
            errors.ValidationError)

    def test_when_model_validate_does_not_raise_then_does_not_raise(self):
        self.validator(User())

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator(None)

    def setup(self):
        self.validator = validators.Model(User)


class User(models.Model):
    name = fields.String()
