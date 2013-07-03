# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from nose.tools import assert_raises_regexp

from booby import Model, fields, errors


class TestModelValidation(object):
    def test_when_login_is_none_then_raises_validation_error(self):
        user = User()

        with assert_raises_regexp(errors.ValidationError, 'required'):
            user.validate()

    def test_when_karma_is_not_an_integer_then_raises_validation_error(self):
        user = User(login='root', karma='max')

        with assert_raises_regexp(errors.ValidationError, 'should be an integer'):
            user.validate()

    def test_when_token_key_is_not_a_string_then_raises_validation_error(self):
        user = User(login='root', token=Token(key=1))

        with assert_raises_regexp(errors.ValidationError, 'should be a string'):
            user.validate()

    def test_when_email_is_an_invalid_email_then_raises_validation_error(self):
        user = User(login='root', email='root@localhost')

        with assert_raises_regexp(errors.ValidationError, 'should be a valid email'):
            user.validate()


class Token(Model):
    key = fields.String()
    secret = fields.String()


class User(Model):
    login = fields.String(required=True)
    email = fields.Email()
    name = fields.String()
    karma = fields.Integer()
    token = fields.Embedded(Token)
