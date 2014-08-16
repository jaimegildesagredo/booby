# -*- coding: utf-8 -*-

from expects import *

from booby import models, fields, encoders

IRRELEVANT_NAME = 'irrelevant name'
IRRELEVANT_EMAIL = 'irrelevant email'


class TestEncode(object):
    def test_should_return_encoded_model(self):
        class User(models.Model):
            name = fields.Field()
            email = fields.Field()

        user = User(name=IRRELEVANT_NAME, email=IRRELEVANT_EMAIL)

        result = self.encoder(user)

        expect(result).to(equal(user.encode()))

    def test_should_return_none_if_value_is_none(self):
        result = self.encoder(None)

        expect(result).to(be_none)

    def setup(self):
        self.encoder = encoders.Model()
