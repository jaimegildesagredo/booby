# -*- coding: utf-8 -*-

from expects import expect

from booby import models, fields, errors
from booby.inspection import inspect


class TestInspect(object):
    def test_instance_should_have_fields_attr_with_the_dict_of_fields(self):
        model = inspect(User())

        expect(model.fields).to.have.keys(name=User.name, email=User.email)

    def test_class_should_have_fields_attr_with_the_dict_of_fields(self):
        model = inspect(User)

        expect(model.fields).to.have.keys(name=User.name, email=User.email)

    def test_fields_attribute_dict_should_not_be_the_internal_model_dict(self):
        model = inspect(User)

        expect(model.fields).not_to.be(User._fields)

    def test_non_model_object_should_raise_inspect_error(self):
        expect(lambda: inspect(object)).to.raise_error(errors.InspectError)


class User(models.Model):
    name = fields.String()
    email = fields.String()
