# -*- coding: utf-8 -*-

from hamcrest import *
from nose.tools import assert_raises

from booby import Model, EmbeddedModel, StringField


class TestEmbeddedModel(object):
    def test_fields(self):
        assert_that(Issue._fields, has_entries(title=Issue.title,
            user=Issue.user))

    def test_init_fields(self):
        issue = Issue(title=u'foo')

        assert_that(issue.title, is_(u'foo'))

    def test_init_default_values(self):
        issue = Issue()

        assert_that(issue.title, is_(None))
        assert_that(issue.user, is_(instance_of(User)))
        assert_that(issue.user.name, is_(None))

    def test_init_embedded_model_fields_with_dict(self):
        issue = Issue(title=u'foo', user={'name': u'Jack'})

        assert_that(issue.title, is_(u'foo'))
        assert_that(issue.user.name, is_(u'Jack'))

    def test_init_embedded_model_fields_with_model_instance(self):
        issue = Issue(title=u'foo', user=User(name=u'Jack'))

        assert_that(issue.title, is_(u'foo'))
        assert_that(issue.user.name, is_(u'Jack'))

    def test_set_embedded_model_with_dict(self):
        issue = Issue()
        issue.user = {'name': u'Jack'}

        assert_that(issue.user.name, is_(u'Jack'))

    def test_set_embedded_model_with_model_instance(self):
        issue = Issue()
        issue.user = User(name=u'Jack')

        assert_that(issue.user.name, is_(u'Jack'))

    def test_set_embedded_model_with_dict_with_invalid_key_raises_value_error(self):
        issue = Issue()

        with assert_raises(ValueError):
            issue.user = {'invalid': u'foo'}

    def test_set_embedded_model_with_invalid_object_raises_value_error(self):
        issue = Issue()

        with assert_raises(ValueError):
            issue.user = object()

    def test_set_embedded_model_field_value(self):
        issue = Issue()
        issue.user.name = u'Jack'

        assert_that(issue.user.name, is_(u'Jack'))

    def test_set_embedded_model_field_value_in_different_instances(self):
        issue = Issue()
        issue.user.name = u'Jack'

        another = Issue()
        another.user.name = u'Bob'

        assert_that(issue.user.name, is_not(another.user.name))

    def test_validate_without_required_field_in_embedded_model_raises_value_error(self):
        issue = Issue()

        with assert_raises(ValueError):
            issue.validate()


class User(Model):
    name = StringField(required=True)


class Issue(Model):
    title = StringField()
    user = EmbeddedModel(User)
