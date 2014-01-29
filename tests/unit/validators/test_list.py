# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import collections

from expects import expect
from .._helpers import stub_validator

from booby import validators, errors


class TestList(object):
    def test_should_pass_if_value_is_a_list(self):
        self.validator(['foo', 'bar'])

    def test_should_pass_if_value_is_a_mutable_sequence(self):
        self.validator(MyList('foo', 'bar'))

    def test_should_fail_if_value_is_not_a_list(self):
        expect(lambda: self.validator(object())).to.raise_error(
            errors.ValidationError, 'should be a list')

    def test_should_fail_if_value_is_none(self):
        expect(lambda: self.validator(None)).to.raise_error(
            errors.ValidationError, 'should be a list')

    def test_should_fail_if_inner_validator_fails(self):
        def inner_validator(value):
            if value == 'bar':
                raise errors.ValidationError('invalid')

        self.validator = validators.List(stub_validator, inner_validator)

        expect(lambda: self.validator(['foo', 'bar'])).to.raise_error(
            errors.ValidationError, 'invalid')

    def setup(self):
        self.validator = validators.List()


class MyList(collections.MutableSequence):
    def __init__(self, *args):
        self._store = list(args)

    def __getitem__(self, index):
        return self._store[index]

    def __setitem__(self, index, value):
        pass

    def __delitem__(self, index):
        pass

    def __len__(self):
        pass

    def insert(self, index, value):
        pass
