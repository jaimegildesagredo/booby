# -*- coding: utf-8 -*-

import datetime

from expects import *

from booby import validators, errors

IRRELEVANT_DATETIME = datetime.datetime.utcnow()
IRRELEVANT_STRING = 'irrelevant string'
IRRELEVANT_DATE = datetime.date.today()


class TestDateTime(object):
    def test_should_pass_if_value_is_a_datetime(self):
        self.validator(IRRELEVANT_DATETIME)

    def test_should_pass_if_value_is_none(self):
        self.validator(None)

    def test_should_fail_if_value_is_a_string(self):
        callback = lambda: self.validator(IRRELEVANT_STRING)

        expect(callback).to(raise_error(errors.ValidationError))

    def test_should_fail_if_value_is_a_date(self):
        callback = lambda: self.validator(IRRELEVANT_DATE)

        expect(callback).to(raise_error(errors.ValidationError))

    def setup(self):
        self.validator = validators.DateTime()
