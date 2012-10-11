# -*- coding: utf-8 -*-

from hamcrest import *
from tests.unit.test_embedded_model import TestEmbeddedModel, TestDictEmbeddedModel

from booby import Model, StringField


class Issue(Model):
    title = StringField()

    class user(Model):
        name = StringField(required=True)


class TestInlineEmbeddedModel(TestEmbeddedModel):
    Issue = Issue
    User = Issue.user.model

    class UserMixin(object):
        user = Issue.user.model


class TestInlineDictEmbeddedModel(TestDictEmbeddedModel):
    Issue = Issue
