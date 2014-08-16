# -*- coding: utf-8 -*-

from expects import *

from booby import models, fields
from booby.inspection import get_fields, is_model


class TestGetFields(object):
    def test_should_return_model_instance_fields_dict(self):
        result = get_fields(User())

        expect(result).to(have_keys(name=User.name, email=User.email))

    def test_should_return_model_class_fields_dict(self):
        result = get_fields(User)

        expect(result).to(have_keys(name=User.name, email=User.email))

    def test_should_return_a_copy_of_internal_fields_dict(self):
        expect(get_fields(User)).not_to(be(get_fields(User)))

    def test_non_model_object_should_raise_type_error(self):
        expect(lambda: get_fields(object)).to(raise_error(TypeError))


class TestIsModel(object):
    def test_should_return_true_if_object_is_a_model_instance(self):
        expect(is_model(User())).to(be_true)

    def test_should_return_true_if_object_is_a_model_subclass(self):
        expect(is_model(User)).to(be_true)

    def test_should_return_false_if_object_isnt_a_model_subclass(self):
        expect(is_model(object)).to(be_false)

    def test_should_return_false_if_object_isnt_a_model_instance(self):
        expect(is_model(object())).to(be_false)


class User(models.Model):
    name = fields.String()
    email = fields.String()
