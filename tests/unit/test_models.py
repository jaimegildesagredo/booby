# -*- coding: utf-8 -*-

from hamcrest import *
from nose.tools import assert_raises_regexp

from booby import Model, StringField


class TestModel(object):
    def test_fields(self):
        assert_that(User._fields, has_entries(name=User.name, email=User.email))

    def test_init_fields(self):
        user = User(name=u'foo', email=u'foo@example.com')

        assert_that(user.name, is_(u'foo'))
        assert_that(user.email, is_(u'foo@example.com'))

    def test_init_default_values(self):
        user = User()

        assert_that(user.name, is_(None))
        assert_that(user.email, is_(None))

    def test_stored_data(self):
        user = User(name=u'foo')
        another = User(name=u'bar')

        assert_that(user.name, is_not(another.name))

    def test_init_invalid_field_raises_value_error(self):
        with assert_raises_regexp(ValueError, "Invalid field 'invalid'"):
            User(invalid=u'foo')

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


class User(Model):
    name = StringField()
    email = StringField()


class UserMixin(object):
    name = StringField()
