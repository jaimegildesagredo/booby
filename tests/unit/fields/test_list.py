# -*- coding: utf-8 -*-

from expects import expect

from booby import fields, models, validators, errors


class TestDefault(object):
    def test_should_be_a_list(self):
        user = User()

        expect(user).to.have.property('emails').with_value.equal([])

    def test_shouldnt_be_the_same_list_for_different_instances(self):
        user1, user2 = User(), User()

        expect(user1.emails).not_to.be(user2.emails)

    def test_should_be_object_passed_as_default(self):
        default = object()

        class User(models.Model):
            emails = fields.List(default=default)

        user = User()

        expect(user).to.have.property('emails').with_value.equal(default)


class TestValidation(object):
    def test_should_pass_if_is_an_empty_list(self):
        self.validate([])

    def test_should_pass_if_is_a_list_of_objects(self):
        self.validate([object(), object()])

    def test_should_raise_validation_error_if_not_a_list(self):
        expect(lambda: self.validate('foo')).to.raise_error(
            errors.ValidationError, 'should be a list')

    def test_should_pass_if_pass_list_inner_validators(self):
        self.field = fields.List(inner_validators=[validators.String()])

        self.validate(['foo', 'bar'])

    def test_should_raise_validation_error_if_inner_validator_raise(self):
        self.field = fields.List(inner_validators=[validators.String()])

        expect(lambda: self.validate(['foo', object()])).to.raise_error(
            errors.ValidationError, 'string')

    def test_should_pass_if_pass_field_validators(self):
        self.field = fields.List(validators.Required())

        self.validate(['foo', 'bar'])

    def test_should_raise_validation_error_if_field_validator_raise(self):
        self.field = fields.List(validators.Required())

        expect(lambda: self.validate(None)).to.raise_error(
            errors.ValidationError, 'required')

    def validate(self, value):
        self.field.validate(value)

    def setup(self):
        self.field = fields.List()


class User(models.Model):
    name = fields.String(default='nobody')
    emails = fields.List()
