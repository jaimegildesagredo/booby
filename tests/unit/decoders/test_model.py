# -*- coding: utf-8 -*-

from expects import *

from booby import models, fields, decoders

IRRELEVANT_NAME = 'irrelevant name'
IRRELEVANT_EMAIL = 'irrelevant email'


class TestDecode(object):
    def test_should_return_none_if_value_is_none(self):
        result = self.decoder(None)

        expect(result).to(be_none)

    def test_should_return_value_returned_by_model_decode(self):
        raw_user = {'name': IRRELEVANT_NAME, 'email': IRRELEVANT_EMAIL}

        result = self.decoder(raw_user)

        expect(result).to(equal(User.decode(raw_user)))

    def setup(self):
        self.decoder = decoders.Model(User)


class User(models.Model):
    name = fields.Field()
    email = fields.Field()

    @classmethod
    def decode(self, value):
        return {
            'foo': 'bar'
        }
