# -*- coding: utf-8 -*-

from hamcrest import *
from nose.tools import assert_raises, assert_raises_regexp

from booby import errors, Model, EmbeddedModel, StringField


class User(Model):
    name = StringField(required=True)


class Issue(Model):
    title = StringField()
    user = EmbeddedModel(User)


class TestEmbeddedModel(object):
    Issue = Issue
    User = User

    class UserMixin(object):
        user = EmbeddedModel(User)

    def test_fields(self):
        assert_that(self.Issue._fields, has_entries(title=self.Issue.title,
            user=self.Issue.user))

    def test_init_fields(self):
        issue = self.Issue(title=u'foo')

        assert_that(issue.title, is_(u'foo'))

    def test_init_default_values(self):
        issue = self.Issue()

        assert_that(issue.title, is_(None))
        assert_that(issue.user, is_(instance_of(self.User)))
        assert_that(issue.user.name, is_(None))

    def test_init_embedded_model_fields_with_dict(self):
        issue = self.Issue(title=u'foo', user={'name': u'Jack'})

        assert_that(issue.title, is_(u'foo'))
        assert_that(issue.user.name, is_(u'Jack'))

    def test_init_embedded_model_fields_with_model_instance(self):
        issue = self.Issue(title=u'foo', user=self.User(name=u'Jack'))

        assert_that(issue.title, is_(u'foo'))
        assert_that(issue.user.name, is_(u'Jack'))

    def test_set_embedded_model_with_dict(self):
        issue = self.Issue()
        issue.user = {'name': u'Jack'}

        assert_that(issue.user.name, is_(u'Jack'))

    def test_set_embedded_model_with_model_instance(self):
        issue = self.Issue()
        issue.user = self.User(name=u'Jack')

        assert_that(issue.user.name, is_(u'Jack'))

    def test_set_embedded_model_with_dict_with_invalid_key_raises_value_error(self):
        issue = self.Issue()

        with assert_raises(ValueError):
            issue.user = {'invalid': u'foo'}

    def test_set_embedded_model_with_invalid_object_raises_value_error(self):
        issue = self.Issue()

        with assert_raises(ValueError):
            issue.user = object()

    def test_set_embedded_model_field_value(self):
        issue = self.Issue()
        issue.user.name = u'Jack'

        assert_that(issue.user.name, is_(u'Jack'))

    def test_set_embedded_model_field_value_in_different_instances(self):
        issue = self.Issue()
        issue.user.name = u'Jack'

        another = self.Issue()
        another.user.name = u'Bob'

        assert_that(issue.user.name, is_not(another.user.name))

    def test_inherit_embedded_models(self):
        class IssueWithSummary(self.Issue):
            summary = StringField()

        assert_that(IssueWithSummary._fields, has_entries(
            user=IssueWithSummary.user,
            title=IssueWithSummary.title,
            summary=IssueWithSummary.summary)
        )

    def test_overwrite_inherited_embedded_models(self):
        class IssueWithSummary(self.Issue):
            summary = StringField()
            user = StringField()

        assert_that(IssueWithSummary.user, is_not(self.Issue.user))

    def test_inherit_mixin_embedded_models(self):
        class Issue(Model, self.UserMixin):
            title = StringField()

        assert_that(Issue._fields, has_entries(
            user=Issue.user,
            title=Issue.title))

    def test_overwrite_inherited_mixin_embedded_models(self):
        class Issue(Model, self.UserMixin):
            title = StringField()
            user = StringField()

        assert_that(Issue.user, is_not(self.UserMixin.user))

    def test_validate_without_required_field_in_embedded_model_raises_validation_error(self):
        issue = self.Issue()

        with assert_raises_regexp(errors.ValidationError, 'required'):
            issue.validate()


class TestDictEmbeddedModel(object):
    Issue = Issue

    def test_to_dict_returns_dict_with_field_values(self):
        issue = self.Issue(title=u'foo', user={'name': u'Jack'})

        assert_that(issue.to_dict(), has_entries(
            title=u'foo',
            user=has_entry('name', u'Jack')
        ))
