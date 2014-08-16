# -*- coding: utf-8 -*-

from expects import *

from booby.helpers import nullable

IRRELEVANT_VALUE = 'irrelevant value'
IRRELEVANT_VALUE2 = 'irrelevant value 2'


class TestNullable(object):
    def test_should_call_method_if_value_is_not_none(self):
        self.method(IRRELEVANT_VALUE)

        expect(self.called).to(be_true)

    def test_should_return_method_returned_value_if_value_is_not_none(self):
        expect(self.method(IRRELEVANT_VALUE)).to(equal(IRRELEVANT_VALUE2))

    def test_shouldnt_call_method_if_value_is_none(self):
        self.method(None)

        expect(self.called).to(be_false)

    def test_should_return_none_if_value_is_none(self):
        expect(self.method(None)).to(be_none)

    @nullable
    def method(self, value):
        self.called = True
        return IRRELEVANT_VALUE2

    def setup(self):
        self.called = False
