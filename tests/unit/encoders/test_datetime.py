# -*- coding: utf-8 -*-

import datetime

from expects import *

from booby import encoders

CUSTOM_FORMAT = '%d/%m/%Y %H:%M:%S'
INVALID_FORMAT = 'invalid format'
IRRELEVANT_DATETIME = datetime.datetime(
    year=2013, month=2, day=13, hour=15, minute=55, second=37)

IRRELEVANT_DATETIME_IN_ISO = IRRELEVANT_DATETIME.isoformat()
IRRELEVANT_DATETIME_IN_CUSTOM_FORMAT = IRRELEVANT_DATETIME.strftime(CUSTOM_FORMAT)
DATETIME_WITH_MICROSECOND = datetime.datetime(
    year=2013, month=2, day=13, hour=15, minute=55, second=37, microsecond=12345)

DATETIME_WITH_MICROSECOND_IN_ISO = DATETIME_WITH_MICROSECOND.isoformat()


class TestEncode(object):
    def test_should_return_datetime_string_in_iso_format(self):
        result = self.encoder(IRRELEVANT_DATETIME)

        expect(result).to(equal(IRRELEVANT_DATETIME_IN_ISO))

    def test_should_return_datetime_string_in_iso_format_with_microsecond(self):
        result = self.encoder(DATETIME_WITH_MICROSECOND)

        expect(result).to(equal(DATETIME_WITH_MICROSECOND_IN_ISO))

    def test_should_return_none_if_value_is_none(self):
        expect(self.encoder(None)).to(be_none)

    def test_should_return_datetime_string_in_given_format(self):
        self.encoder = encoders.DateTime(CUSTOM_FORMAT)

        result = self.encoder(IRRELEVANT_DATETIME)

        expect(result).to(equal(IRRELEVANT_DATETIME_IN_CUSTOM_FORMAT))

    def setup(self):
        self.encoder = encoders.DateTime()
