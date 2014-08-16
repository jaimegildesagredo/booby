# -*- coding: utf-8 -*-

from expects import *

from booby import errors


class String(object):
    def test_should_pass_if_value_is_none(self):
        self.validator(None)

    def test_should_fail_if_value_is_not_a_string(self):
        expect(lambda: self.validator(1)).to(raise_error(
            errors.ValidationError, 'should be a string'))
