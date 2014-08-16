# -*- coding: utf-8 -*-

from expects import *

from booby import fields, models


IRRELEVANT_NAME = 'irrelevant name'
IRRELEVANT_EMAIL = 'irrelevant email'
DECODED_IRRELEVANT_NAME = 'decoded irrelevant name'
DECODED_IRRELEVANT_EMAIL = 'decoded irrelevant email'


class TestDecodeModel(object):
    def test_should_use_value_returned_by_field_decode_method(self):
        class User(models.Model):
            name = StubField(decoded=DECODED_IRRELEVANT_NAME)
            email = StubField(decoded=DECODED_IRRELEVANT_EMAIL)

        result = User.decode({
            'name': IRRELEVANT_NAME,
            'email': IRRELEVANT_EMAIL
        })

        expect(result).to(have_keys(name=DECODED_IRRELEVANT_NAME,
                                    email=DECODED_IRRELEVANT_EMAIL))

    def test_should_return_dict_with_model_mapped_fields(self):
        class User(models.Model):
            name = fields.Field(name='username')
            email = fields.Field(name='emailAddress')

        result = User.decode({
            'username': IRRELEVANT_NAME,
            'emailAddress': IRRELEVANT_EMAIL
        })

        expect(result).to(have_keys(name=IRRELEVANT_NAME,
                                    email=IRRELEVANT_EMAIL))

    def test_should_return_dict_with_model_fields_if_field_is_missing(self):
        class User(models.Model):
            name = fields.Field()
            email = fields.Field()

        result = User.decode({'name': IRRELEVANT_NAME})

        expect(result).to(have_keys(name=IRRELEVANT_NAME))


class StubField(fields.Field):
    def decode(self, value):
        return self.options['decoded']
