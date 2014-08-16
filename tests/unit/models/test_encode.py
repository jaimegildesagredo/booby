# -*- coding: utf-8 -*-

from expects import expect

from booby import fields, models


IRRELEVANT_NAME = 'irrelevant name'
IRRELEVANT_EMAIL = 'irrelevant email'
ENCODED_IRRELEVANT_NAME = 'encoded irrelevant name'
ENCODED_IRRELEVANT_EMAIL = 'encoded irrelevant email'


class TestEncodeModel(object):
    def test_should_use_value_returned_by_field_encode_method(self):
        class User(models.Model):
            name = StubField(encoded=ENCODED_IRRELEVANT_NAME)
            email = StubField(encoded=ENCODED_IRRELEVANT_EMAIL)

        user = User(name=IRRELEVANT_NAME, email=IRRELEVANT_EMAIL)

        result = user.encode()

        expect(result).to.have.keys(name=ENCODED_IRRELEVANT_NAME,
                                    email=ENCODED_IRRELEVANT_EMAIL)

    def test_should_return_dict_with_model_mapped_fields(self):
        class User(models.Model):
            name = fields.Field(name='username')
            email = fields.Field(name='emailAddress')

        user = User(name=IRRELEVANT_NAME, email=IRRELEVANT_EMAIL)

        result = user.encode()

        expect(result).to.have.keys(username=IRRELEVANT_NAME,
                                    emailAddress=IRRELEVANT_EMAIL)


class StubField(fields.Field):
    def encode(self, value):
        return self.options['encoded']
