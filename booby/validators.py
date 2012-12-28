# -*- coding: utf-8 -*-
#
# Copyright 2012 Jaime Gil de Sagredo Luna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The `validators` module contains a set of :mod:`fields` validators.

A validator is any `object` with a :func:`validate` method which receives
a `value` as the target for the validation. If the validation fails then
the :func:`validate` method should raise an :class:`errors.ValidationError`
exception with an error message.

`Validators` are passed to :class:`fields.Field` and subclasses as possitional
arguments.

"""

from booby import errors


class Required(object):
    """This validator forces fields to have a value other than `None`."""

    def validate(self, value):
        if value is None:
            raise errors.ValidationError('is required')


class In(object):
    """This validator forces fields to have their value in the given list.

    :param choices: A `list` of possible values.

    """

    def __init__(self, choices):
        self.choices = choices

    def validate(self, value):
        if value not in self.choices:
            raise errors.ValidationError('should be in {}'.format(self.choices))


class String(object):
    """This validator forces fields values to be an instance of `basestring`."""

    def validate(self, value):
        if value is not None and not isinstance(value, basestring):
            raise errors.ValidationError('should be a string')


class Integer(object):
    """This validator forces fields values to be an instance of `int`."""

    def validate(self, value):
        if value is not None and not isinstance(value, int):
            raise errors.ValidationError('should be an integer')


class Float(object):
    """This validator forces fields values to be an instance of `float`."""

    def validate(self, value):
        if value is not None and not isinstance(value, float):
            raise errors.ValidationError('should be a float')


class Boolean(object):
    """This validator forces fields values to be an instance of `bool`."""

    def validate(self, value):
        if value is not None and not isinstance(value, bool):
            raise errors.ValidationError('should be a boolean')


class Embedded(object):
    """This validator forces fields values to be an instance of the given
    `model` and also performs a validation in the entire model object.

    :param model: An instance of :class:`models.Model`

    """

    def __init__(self, model):
        self.model = model

    def validate(self, value):
        if value is None:
            return

        if not isinstance(value, self.model):
            raise errors.ValidationError(
                "should be an instance of '{}'".format(self.model.__name__))

        value.validate()
