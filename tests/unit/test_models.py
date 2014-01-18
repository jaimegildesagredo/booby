# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json

from expects import expect

from booby import errors, fields, models


class TestDefaultModelInit(object):
    def test_when_pass_kwargs_then_set_fields_values(self):
        user = User(name='foo', email='foo@example.com')

        expect(user.name).to.equal('foo')
        expect(user.email).to.equal('foo@example.com')

    def test_when_pass_kwargs_without_required_field_then_required_field_is_none(self):
        user = UserWithRequiredName(email='foo@example.com')

        expect(user.name).to.equal(None)

    def test_when_pass_invalid_field_in_kwargs_then_raises_field_error(self):
        expect(lambda: User(foo='bar')).to.raise_error(
            errors.FieldError, 'foo')


class TestOverridenModelInit(object):
    def test_when_pass_args_then_set_fields_values(self):
        class UserWithOverridenInit(User):
            def __init__(self, name, email):
                self.name = name
                self.email = email

        user = UserWithOverridenInit('foo', 'foo@example.com')

        expect(user.name).to.equal('foo')
        expect(user.email).to.equal('foo@example.com')


class TestModelData(object):
    def test_when_set_field_value_then_another_model_shouldnt_have_the_same_value(self):
        user = User(name='foo')
        another = User(name='bar')

        expect(user.name).not_to.equal(another.name)


class TestValidateModel(object):
    def test_when_validate_and_validation_errors_then_raises_first_validation_error(self):
        user = UserWithRequiredName(email='foo@example.com')

        expect(lambda: user.validate()).to.raise_error(
            errors.ValidationError, 'required')

    def test_when_validate_without_errors_then_does_not_raise(self):
        user = UserWithRequiredName(name='Jack')

        user.validate()

    def test_when_is_valid_and_validation_errors_then_is_false(self):
        user = UserWithRequiredName(email='foo@example.com')

        expect(user.is_valid).to.be.false

    def test_when_is_valid_and_not_validation_errors_then_is_true(self):
        user = UserWithRequiredName(name='Jack')

        expect(user.is_valid).to.be.true

    def test_when_validation_errors_and_errors_then_has_pairs_of_name_and_errors(self):
        user = UserWithRequiredFields(id=1, role='root')

        errors = dict(user.validation_errors)

        expect(errors['id']).to.have('be a string')
        expect(errors['role']).to.have('be in')
        expect(errors['name']).to.have('required')

    def test_when_validation_errors_and_no_errors_then_returns_none(self):
        user = UserWithRequiredName(name='jack')

        errors = user.validation_errors

        expect(errors).to.be.empty


class TestInheritedModel(object):
    def test_when_pass_kwargs_then_set_fields_values(self):
        user = UserWithPage(name='foo', email='foo@example.com', page='example.com')

        expect(user.name).to.equal('foo')
        expect(user.email).to.equal('foo@example.com')
        expect(user.page).to.equal('example.com')

    def test_when_pass_invalid_field_in_kwargs_then_raises_field_error(self):
        expect(lambda: UserWithPage(foo='bar')).to.raise_error(
            errors.FieldError, 'foo')

    def test_when_override_superclass_field_then_validates_subclass_field(self):
        class UserWithoutRequiredName(UserWithRequiredName):
            name = fields.String()

        user = UserWithoutRequiredName()
        user.validate()


class TestInheritedMixin(object):
    def test_when_pass_kwargs_then_set_fields_values(self):
        user = UserWithEmail(name='foo', email='foo@example.com')

        expect(user).to.have.properties(name='foo', email='foo@example.com')

    def test_when_pass_invalid_field_in_kwargs_then_raises_field_error(self):
        expect(lambda: UserWithEmail(foo='bar')).to.raise_error(
            errors.FieldError, 'foo')

    def test_when_override_mixin_field_then_validates_subclass_field(self):
        class User(UserMixin, models.Model):
            name = fields.String(required=True)

        user = User()

        expect(lambda: user.validate()).to.raise_error(
            errors.ValidationError, 'required')


class TestDictModel(object):
    def test_when_get_field_then_returns_value(self):
        expect(self.user['name']).to.equal('foo')

    def test_when_get_invalid_field_then_raises_field_error(self):
        expect(lambda: self.user['foo']).to.raise_error(
            errors.FieldError, 'foo')

    def test_when_set_field_then_update_field_value(self):
        self.user['name'] = 'bar'

        expect(self.user).to.have.property('name', 'bar')

    def test_when_set_invalid_field_then_raises_field_error(self):
        def callback():
            self.user['foo'] = 'bar'

        expect(callback).to.raise_error(errors.FieldError, 'foo')

    def test_when_update_with_dict_then_update_fields_values(self):
        self.user.update({'name': 'foobar', 'email': 'foo@bar.com'})

        expect(self.user).to.have.properties(name='foobar', email='foo@bar.com')

    def test_when_update_kw_arguments_then_update_fields_values(self):
        self.user.update(name='foobar', email='foo@bar.com')

        expect(self.user).to.have.properties(name='foobar', email='foo@bar.com')

    def test_when_update_invalid_field_then_raises_field_error(self):
        expect(lambda: self.user.update(foo='bar')).to.raise_error(
            errors.FieldError, 'foo')

    def setup(self):
        self.user = User(name='foo', email='roo@example.com')


class TestModelToDict(object):
    def test_when_model_has_single_fields_then_returns_dict_with_fields_values(self):
        user = dict(User(name='foo', email='roo@example.com'))

        expect(user).to.have.keys(name='foo', email='roo@example.com')

    def test_when_model_has_embedded_model_field_then_returns_dict_with_inner_dict(self):
        class UserWithToken(User):
            token = fields.Field()

        user = dict(UserWithToken(name='foo', email='roo@example.com',
                                  token=self.token1))

        expect(user).to.have.keys(name='foo', email='roo@example.com',
                                  token=dict(self.token1))

    def test_when_model_has_list_of_models_then_returns_list_of_dicts(self):
        user = dict(UserWithList(tokens=[self.token1, self.token2]))

        expect(user['tokens']).to.have(dict(self.token1), dict(self.token2))

    def test_when_model_has_list_of_models_and_values_then_returns_list_of_dicts_and_values(self):
        user = dict(UserWithList(tokens=[self.token1, 'foo', self.token2]))

        expect(user['tokens']).to.have(dict(self.token1), 'foo',
                                       dict(self.token2))

    def setup(self):
        self.token1 = Token(key='foo', secret='bar')
        self.token2 = Token(key='fuu', secret='baz')


class TestModelToJSON(object):
    def test_when_model_has_single_fields_then_returns_json_with_fields_values(self):
        result = self.user.to_json()

        expect(result).to.equal(json.dumps(dict(self.user)))

    def test_when_pass_extra_arguments_then_call_json_dump_function_with_these_args(self):
        result = self.user.to_json(indent=2)

        expect(result).to.equal(json.dumps(dict(self.user), indent=2))

    def setup(self):
        self.user = User(name='Jack', email='jack@example.com')


class TestSource(object):
    def test_when_pass_mapped_kwargs_then_set_fields_values(self):
        user = UserWithSource(name='foo', emailAddress='foo@example.com')

        expect(user.name).to.equal('foo')
        expect(user.email).to.equal('foo@example.com')

    def test_when_model_has_source_then_returns_dict_with_mapped_field_name(self):
        user = dict(UserWithSource(name='Jack', emailAddress='jack@example.com'))

        expect(user).to.have.keys(name='Jack', emailAddress='jack@example.com')


class User(models.Model):
    name = fields.String()
    email = fields.String()


class UserWithRequiredName(User):
    name = fields.String(required=True)


class UserWithRequiredFields(UserWithRequiredName):
    id = fields.String()
    role = fields.String(choices=['admin', 'user'])


class UserWithSource(models.Model):
    name = fields.String()
    email = fields.String(source='emailAddress')


class UserWithPage(User):
    page = fields.String()


class UserMixin(object):
    name = fields.String()


class UserWithEmail(UserMixin, models.Model):
    email = fields.String()


class UserWithList(User):
    tokens = fields.Field()


class Token(models.Model):
    key = fields.String()
    secret = fields.String()
