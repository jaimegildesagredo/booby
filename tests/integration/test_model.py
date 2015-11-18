# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from expects import *

from booby import models, fields, errors

IRRELEVANT_TOKEN = {
    'key': 'foo',
    'secret': 'bar'
}


class TestValidation(object):
    def test_should_fail_validation_if_login_is_none(self):
        def callback():
            User().validate()

        expect(callback).to(raise_error(
            errors.ValidationError, end_with('required')))

    def test_should_fail_validation_if_karma_is_not_an_integer(self):
        def callback():
            user = User(login='root', karma='max')
            user.validate()

        expect(callback).to(raise_error(errors.ValidationError,
                                        'karma should be an integer'))

    def test_should_fail_validation_if_token_key_is_not_a_string(self):
        def callback():
            user = User(login='root', token=Token(key=1))
            user.validate()

        expect(callback).to(raise_error(errors.ValidationError,
                                        'token key should be a string'))

    def test_should_fail_validation_if_invalid_email(self):
        def callback():
            user = User(login='root', email='@localhost')
            user.validate()

        expect(callback).to(raise_error(errors.ValidationError,
                                        'email should be a valid email'))


class TestEncode(object):
    def test_should_return_dict_with_encoded_token(self):
        user = User(token=IRRELEVANT_TOKEN)

        result = user.encode()

        expect(result['token']).to(have_keys(IRRELEVANT_TOKEN))

    def test_should_return_dict_with_encoded_friends(self):
        friends =  [Friend(), Friend()]
        user = User(friends=friends)

        result = user.encode()

        expect(result['friends']).to(equal(
            [friends[0].encode(), friends[1].encode()]))


class Token(models.Model):
    key = fields.String()
    secret = fields.String()


class Friend(models.Model):
    name = fields.String()


class User(models.Model):
    login = fields.String(required=True)
    email = fields.Email()
    karma = fields.Integer()
    token = fields.Embedded(Token)
    friends = fields.Collection(Friend)
