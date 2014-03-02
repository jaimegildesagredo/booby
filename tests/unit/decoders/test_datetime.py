# -*- coding: utf-8 -*-

import datetime

from expects import expect

from booby import decoders, errors

CUSTOM_FORMAT = '%d/%m/%Y %H:%M:%S'
IRRELEVANT_DATETIME = datetime.datetime(
    year=2013, month=2, day=13, hour=15, minute=55, second=37)

IRRELEVANT_DATETIME_IN_ISO = IRRELEVANT_DATETIME.isoformat()
IRRELEVANT_DATETIME_IN_CUSTOM_FORMAT = IRRELEVANT_DATETIME.strftime(CUSTOM_FORMAT)
DATETIME_WITH_MICROSECOND = datetime.datetime(
    year=2013, month=2, day=13, hour=15, minute=55, second=37, microsecond=12345)

DATETIME_WITH_MICROSECOND_IN_ISO = DATETIME_WITH_MICROSECOND.isoformat()
INVALID_DATETIME_STRING = 'invalid datetime string'


class TestDecode(object):
    def test_should_return_datetime_from_string_in_iso_format(self):
        result = self.decoder(IRRELEVANT_DATETIME_IN_ISO)

        expect(result).to.equal(IRRELEVANT_DATETIME)

    def test_should_return_datetime_with_microsecond_from_string_in_iso_format(self):
        result = self.decoder(DATETIME_WITH_MICROSECOND_IN_ISO)

        expect(result).to.equal(DATETIME_WITH_MICROSECOND)

    def test_should_return_none_if_value_is_none(self):
        expect(self.decoder(None)).to.be.none

    def test_should_raise_decode_error_if_value_does_not_match_iso_format(self):
        def callback():
            self.decoder(INVALID_DATETIME_STRING)

        expect(callback).to.raise_error(errors.DecodeError)

    def test_should_return_datetime_with_given_format(self):
        self.decoder = decoders.DateTime(CUSTOM_FORMAT)

        result = self.decoder(IRRELEVANT_DATETIME_IN_CUSTOM_FORMAT)

        expect(result).to.equal(IRRELEVANT_DATETIME)

    def setup(self):
        self.decoder = decoders.DateTime()
