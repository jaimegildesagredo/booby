# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from expects import *
from . import mixins

from booby import validators, errors


class TestEmail(mixins.String):
    def test_should_pass_if_value_is_valid_email(self):
        self.validator('foo2bar@example.com')

    def test_should_pass_if_value_contains_plus_sign(self):
        self.validator('foo+bar@example.com')

    def test_should_pass_if_value_contains_minus_sign(self):
        self.validator('foo-bar@example.com')

    def test_should_pass_if_domain_is_tld(self):
        self.validator('foo@example')

    def test_should_fail_if_nothing_before_at_sign(self):
        expect(lambda: self.validator('@example')).to(raise_error(
            errors.ValidationError, 'should be a valid email'))

    def test_should_fail_if_value_doesnt_have_at_sign(self):
        expect(lambda: self.validator('foo%example.com')).to(raise_error(
            errors.ValidationError, 'should be a valid email'))

    def test_should_fail_if_empty_string(self):
        expect(lambda: self.validator('')).to(raise_error(
            errors.ValidationError, 'should be a valid email'))

    def setup(self):
        self.validator = validators.Email()
