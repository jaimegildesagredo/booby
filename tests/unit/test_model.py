# -*- coding: utf-8 -*-

from hamcrest import *
from nose.tools import assert_raises_regexp

from booby import Model, StringField


class TestModel(object):
    def test_fields(self):
        assert_that(User._fields, has_entries(name=User.name, email=User.email))

    def test_sets_fields_names(self):
        assert_that(User.name.name, is_('name'))
        assert_that(User.email.name, is_('email'))

    def test_init_fields(self):
        user = User(name=u'foo', email=u'foo@example.com')

        assert_that(user.name, is_(u'foo'))
        assert_that(user.email, is_(u'foo@example.com'))

    def test_init_default_values(self):
        user = User()

        assert_that(user.name, is_(None))
        assert_that(user.email, is_(None))

    def test_init_without_required_values(self):
        user = UserWithRequiredName(email='foo@example.com')

        assert_that(user.name, is_(None))

    def test_init_invalid_field_raises_value_error(self):
        with assert_raises_regexp(ValueError, "Invalid field 'invalid'"):
            User(invalid=u'foo')

    def test_stored_data(self):
        user = User(name=u'foo')
        another = User(name=u'bar')

        assert_that(user.name, is_not(another.name))

    def test_inherit_model_fields(self):
        class UserWithPage(User):
            page = StringField()

        assert_that(UserWithPage._fields, has_entries(name=UserWithPage.name,
            email=UserWithPage.email, page=UserWithPage.page))

    def test_overwrite_inherited_model_fields(self):
        class UserWithPage(User):
            name = StringField()
            page = StringField()

        assert_that(UserWithPage.name, is_not(User.name))
        assert_that(UserWithPage._fields, has_entries(name=UserWithPage.name,
            email=UserWithPage.email))

    def test_sets_inherited_model_fields_names(self):
        class UserWithPage(User):
            page = StringField()

        assert_that(UserWithPage.page.name, is_('page'))
        assert_that(UserWithPage.name.name, is_('name'))
        assert_that(UserWithPage.email.name, is_('email'))

    def test_inherit_mixin_fields(self):
        class UserWithEmail(Model, UserMixin):
            email = StringField()

        assert_that(UserWithEmail._fields, has_entries(name=UserWithEmail.name,
            email=UserWithEmail.email))

    def test_overwrite_inherited_mixin_fields(self):
        class UserWithEmail(UserMixin, Model):
            name = StringField()
            email = StringField()

        assert_that(UserWithEmail.name, is_not(UserMixin.name))
        assert_that(UserWithEmail._fields, has_entries(name=UserWithEmail.name,
            email=UserWithEmail.email))

    def test_sets_inherited_mixin_fields_names(self):
        class UserWithEmail(UserMixin, Model):
            email = StringField()

        assert_that(UserWithEmail.name.name, is_('name'))
        assert_that(UserWithEmail.email.name, is_('email'))

    def test_validate_without_required_values_raises_value_error(self):
        user = UserWithRequiredName(email='foo@example.com')

        with assert_raises_regexp(ValueError, ''):
            user.validate()


class TestDictModel(object):
    def test_get_field_value(self):
        assert_that(self.user['name'], is_(u'foo'))

    def test_get_invalid_field_raises_key_error(self):
        with assert_raises_regexp(ValueError, "Invalid field 'invalid'"):
            self.user['invalid']

    def test_set_field_value(self):
        self.user['name'] = u'bar'

        assert_that(self.user['name'], is_(u'bar'))

    def test_set_invalid_field_raises_key_error(self):
        with assert_raises_regexp(ValueError, "Invalid field 'invalid'"):
            self.user['invalid'] = u'foo'

    def test_update_updates_fields(self):
        self.user.update({'name': u'foobar', 'email': u'foo@bar.com'})

        assert_that(self.user.name, is_(u'foobar'))
        assert_that(self.user.email, is_(u'foo@bar.com'))

    def test_update_kw_fields_updates_fields(self):
        self.user.update(name=u'foobar', email=u'foo@bar.com')

        assert_that(self.user.name, is_(u'foobar'))
        assert_that(self.user.email, is_(u'foo@bar.com'))

    def test_update_invalid_field_raises_value_error(self):
        with assert_raises_regexp(ValueError, "Invalid field 'invalid'"):
            self.user.update(invalid=u'foo')

    def setup(self):
        self.user = User(name=u'foo', email='roo@example.com')


class User(Model):
    name = StringField()
    email = StringField()


class UserMixin(object):
    name = StringField()


class UserWithRequiredName(User):
    name = StringField(required=True)
