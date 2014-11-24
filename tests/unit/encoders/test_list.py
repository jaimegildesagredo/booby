# -*- coding: utf-8 -*-

from expects import *
from .._helpers import MyList

from booby import models, fields, encoders, errors

IRRELEVANT_LIST = [1, 2, 3]
IRRELEVANT_MUTABLE_SEQUENCE = MyList(*IRRELEVANT_LIST)


class TestEncode(object):
    def test_should_return_a_list(self):
        result = self.encoder(IRRELEVANT_LIST)

        expect(result).to(equal(IRRELEVANT_LIST))

    def test_should_return_a_list_given_a_mutable_sequence(self):
        result = self.encoder(IRRELEVANT_MUTABLE_SEQUENCE)

        expect(result).to(equal(IRRELEVANT_LIST))

    def test_should_return_a_list_of_models(self):
        users = [User(), User()]

        result = self.encoder(users)

        expect(result).to(equal(users))

    def test_should_return_a_list_of_encoded_models(self):
        users = [User(), User()]

        self.encoder = encoders.List(encoders.Model())
        result = self.encoder(users)

        expect(result).to(equal([users[0].encode(), users[1].encode()]))

    def test_should_return_none_if_value_is_none(self):
        result = self.encoder(None)

        expect(result).to(be_none)

    def test_should_raise_encode_error_if_value_is_not_a_list(self):
        def callback():
            self.encoder(object())

        expect(callback).to(raise_error(errors.EncodeError))

    def setup(self):
        self.encoder = encoders.List()


class User(models.Model):
    name = fields.Field()
    email = fields.Field()
