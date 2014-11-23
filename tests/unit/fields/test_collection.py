# -*- coding: utf-8 -*-

import collections

from expects import *

from booby import Model, fields, errors
from tests.unit._helpers import MyDict


class TestSetValueInCollectionField(object):
    def test_when_value_is_a_list_of_dicts_then_value_is_a_list_of_models(self):
        users = [{'name': 'Foo'}, {'name': 'Foo'}]
        group = Group(users=users)

        expect(group.users[0]).to(be_an(User) & have_properties(users[0]))
        expect(group.users[1]).to(be_an(User) & have_properties(users[1]))

    def test_when_value_is_a_list_of_mutable_mappings_then_value_is_a_list_of_models(self):
        users = [MyDict(name='Foo'), MyDict(name='Foo')]
        group = Group(users=users)

        expect(group.users[0]).to(be_an(User) & have_properties(users[0]))
        expect(group.users[1]).to(be_an(User) & have_properties(users[1]))

    def test_when_value_is_a_list_of_models_then_the_value_is_a_list_of_the_same_models(self):
        users = [User(name='Foo'), User(name='Foo')]
        group = Group(users=users)

        expect(group.users[0]).to(be(users[0]))
        expect(group.users[1]).to(be(users[1]))

    def test_when_value_is_a_non_list_object_then_value_is_the_same(self):
        users = object()
        group = Group(users=users)

        expect(group.users).to(be(users))


class TestDefaultValue(object):
    def test_should_be_an_empty_list(self):
        expect(Group().users).to(be_a(list) & be_empty)

    def test_shouldnt_be_the_same_list_for_different_instances(self):
        expect(Group().users).not_to(be(Group().users))

    def test_should_be_the_object_passed_as_default_argument(self):
        default = object()

        class Group(Model):
            users = fields.Collection(User, default=default)

        expect(Group().users).to(be(default))


class TestValidate(object):
    def test_should_pass_if_is_an_empty_list(self):
        Group(users=[]).validate()

    def test_should_pass_if_is_a_list_of_models(self):
        Group(users=[User(name='Foo'), User(name='Bar')]).validate()

    def test_should_fail_if_is_not_a_list(self):
        expect(Group(users=object()).validate).to(
            raise_error(errors.ValidationError, contain('list')))

    def test_should_fail_if_is_a_list_of_non_model_objects(self):
        expect(Group(users=[object(), object()]).validate).to(
            raise_error(errors.ValidationError, contain('instance of')))


class TestEncode(object):
    def test_should_return_list_of_encoded_models(self):
        result = Group(users=[User(name='Foo'), User(name='Bar')]).encode()

        expect(result).to(equal({'users': [{'username': 'Foo'}, {'username': 'Bar'}]}))


class TestDecode(object):
    def test_should_return_list_of_decoded_dicts(self):
        result = Group.decode({'users': [{'username': 'Foo'}, {'username': 'Bar'}]})

        expect(result).to(equal({'users': [{'name': 'Foo'}, {'name': 'Bar'}]}))


class User(Model):
    name = fields.Field(name='username')


class Group(Model):
    users = fields.Collection(User)
