# -*- coding: utf-8 -*-

import json
from cStringIO import StringIO

from expects import expect
from booby import models, fields, serialize, errors
from booby.errors import DeSerializationError


class TestSerialize(object):
    def test_when_model_has_allow_serialize_False(self):
        expect(lambda: serialize.serialize(self.user)).to.raise_error(
            errors.SerializationError, "{0} is not serializable".format(repr(self.user)))

    def test_serialization_with_invalid_data(self):
        user = User(name=123, email='jack@example.com')
        expect(lambda: serialize.serialize(user)).to.raise_error(
            errors.SerializationError, "{0} is not serializable".format(repr(user)))

    def test_serialization_with_valid_data(self):
        cls = self.user_meta.__class__
        expect(serialize.serialize(self.user_meta)).to.equal(
            json.dumps([{'model': cls.__module__ + "." + cls.__name__,
                        'obj': dict(self.user_meta)}]))

    def test_serialization_with_valid_data_and_out_file(self):
        _file = StringIO()
        cls = self.user_meta.__class__
        serialize.serialize(self.user_meta, out_file=_file)
        _file.seek(0)
        expect(_file.read()).to.equal(
            json.dumps([{'model': cls.__module__ + "." + cls.__name__,
                        'obj': dict(self.user_meta)}]))

    def setup(self):
        self.user = User(name='Jack', email='jack@example.com')
        self.user_meta = UserWithMeta(name='Jack', email='jack@example.com')


class TestDeSerialize(object):
    def test_json_object_with_no_model_attribute(self):
        expect(lambda: serialize.deserialize(self.user.to_json())).to.raise_error(
                                                          DeSerializationError)

    def test_json_object_from_invalid_data(self):
        user = User(name='Jack', email=123)
        expect(lambda: serialize.deserialize(user.to_json())).to.raise_error(
                                                          DeSerializationError)

    def test_json_object_with_model_doesnt_exist(self):
        dct = self.user_meta.to_dict()
        dct['model'] = 'invalid.model'
        expect(lambda: serialize.deserialize(json.dumps(dct))).to.raise_error(
                                                          DeSerializationError)

    def test_valid_json_object_as_string(self):
        actual = serialize.deserialize(self.user_meta.to_json())
        expect(actual).to.equal([self.user_meta])

    def test_valid_json_object_as_file(self):
        _file = StringIO()
        _file.write(self.user_meta.to_json())
        _file.seek(0)

        actual = serialize.deserialize(_file)
        expect(actual).to.equal([self.user_meta])

    def setup(self):
        self.user = User(name='Jack', email='jack@example.com')
        self.user_meta = UserWithMeta(name='Jack', email='jack@example.com')


class User(models.Model):
    name = fields.String()
    email = fields.String()

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()


class UserWithMeta(User):
    meta = {'allow_serialize': True}
