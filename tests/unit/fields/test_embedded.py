# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from expects import *
from .._helpers import MyDict

from booby import fields, errors, models


class TestEmbeddedFieldDescriptor(object):
    def test_when_set_field_value_with_dict_then_value_is_embedded_object_with_dict_values(self):
        self.group.admin = {'name': 'foo', 'email': 'foo@example.com'}

        expect(self.group.admin).to(be_an(User))
        expect(self.group.admin).to(have_properties(
            name='foo', email='foo@example.com'))

    def test_when_set_field_value_with_dict_with_invalid_field_then_raises_field_error(self):
        def callback():
            self.group.admin = {'name': 'foo', 'foo': 'bar'}

        expect(callback).to(raise_error(errors.FieldError, 'foo'))

    def test_when_set_field_value_with_mutable_mapping_then_value_is_model_instance_with_dict_values(self):
        self.group.admin = MyDict(name='foo', email='foo@example.com')

        expect(self.group.admin).to(be_an(User))
        expect(self.group.admin).to(have_properties(
            name='foo', email='foo@example.com'))

    def test_when_set_field_value_with_not_dict_object_then_value_is_given_object(self):
        user = User(name='foo', email='foo@example.com')
        self.group.admin = user

        expect(self.group.admin).to(be(user))

    def test_when_set_field_with_not_model_instance_then_value_is_given_object(self):
        user = object()
        self.group.admin = user

        expect(self.group.admin).to(be(user))

    def setup(self):
        self.group = Group()


class TestEmbeddedFieldBuiltinValidators(object):
    def test_when_value_is_not_instance_of_model_then_raises_validation_error(self):
        expect(lambda: self.field.validate(object())).to(raise_error(
            errors.ValidationError, match('.*instance of.*')))

    def test_when_embedded_model_field_has_invalid_value_then_raises_validation_error(self):
        expect(lambda: self.field.validate(User(name=1))).to(raise_error(
            errors.ValidationError, match('.*string')))

    def test_when_embedded_model_validates_then_does_not_raise(self):
        self.field.validate(User())

    def setup(self):
        self.field = fields.Embedded(User)


class User(models.Model):
    name = fields.String(default='nobody')
    email = fields.String()


class Group(models.Model):
    name = fields.String()
    admin = fields.Embedded(User)
