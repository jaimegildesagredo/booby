# -*- coding: utf-8 -*-

from nose.tools import assert_raises_regexp

from booby import validators, errors


class TestRequired(object):
    def test_when_value_is_none_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'is required'):
            self.validator.validate(None)

    def test_when_value_is_not_none_then_does_not_raise(self):
        self.validator.validate('foo')

    def setup(self):
        self.validator = validators.Required()


class TestIn(object):
    def test_when_value_is_not_in_choices_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, "should be in \['foo', 'bar'\]"):
            self.validator.validate('baz')

    def test_when_value_is_in_choices_then_does_not_raise(self):
        self.validator.validate('bar')

    def setup(self):
        self.validator = validators.In(['foo', 'bar'])


class TestString(object):
    def test_when_value_is_not_string_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a string'):
            self.validator.validate(1)

    def test_when_value_is_a_string_then_does_not_raise(self):
        self.validator.validate('foo')

    def test_when_value_is_unicode_then_does_not_raise(self):
        self.validator.validate(u'foo')

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator.validate(None)

    def setup(self):
        self.validator = validators.String()


class TestInteger(object):
    def test_when_value_is_not_an_integer_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be an integer'):
            self.validator.validate('foo')

    def test_when_value_is_an_integer_then_does_not_raise(self):
        self.validator.validate(1)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator.validate(None)

    def setup(self):
        self.validator = validators.Integer()


class TestFloat(object):
    def test_when_value_is_not_a_float_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a float'):
            self.validator.validate('foo')

    def test_when_value_is_a_float_then_does_not_raise(self):
        self.validator.validate(1.0)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator.validate(None)

    def setup(self):
        self.validator = validators.Float()


class TestBoolean(object):
    def test_when_value_is_not_a_boolean_then_raises_validation_error(self):
        with assert_raises_regexp(errors.ValidationError, 'should be a boolean'):
            self.validator.validate('foo')

    def test_when_value_is_a_boolean_then_does_not_raises(self):
        self.validator.validate(False)

    def test_when_value_is_none_then_does_not_raise(self):
        self.validator.validate(None)

    def setup(self):
        self.validator = validators.Boolean()
