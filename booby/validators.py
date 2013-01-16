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

import re
import functools

from booby import errors


def nullable(method):
    """This is a helper validation decorator for validators that allow
    their `values` to be :keyword:`None`.

    The :class:`String` validator is a good example::

        class String(object):
            def validate(self, value):
                if value is not None:
                    pass # Do the validation here ...

    Now the same but using the `@nullable` decorator::

        @nullable
        def validate(self, value):
            pass # Do the validation here ...

    """

    @functools.wraps(method)
    def wrapper(self, value):
        if value is not None:
            method(self, value)

    return wrapper


class Required(object):
    """This validator forces fields to have a value other than :keyword:`None`."""

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

    @nullable
    def validate(self, value):
        if not isinstance(value, basestring):
            raise errors.ValidationError('should be a string')


class Integer(object):
    """This validator forces fields values to be an instance of `int`."""

    @nullable
    def validate(self, value):
        if not isinstance(value, int):
            raise errors.ValidationError('should be an integer')


class Float(object):
    """This validator forces fields values to be an instance of `float`."""

    @nullable
    def validate(self, value):
        if not isinstance(value, float):
            raise errors.ValidationError('should be a float')


class Boolean(object):
    """This validator forces fields values to be an instance of `bool`."""

    @nullable
    def validate(self, value):
        if not isinstance(value, bool):
            raise errors.ValidationError('should be a boolean')


class Model(object):
    """This validator forces fields values to be an instance of the given
    :class:`models.Model` subclass and also performs a validation in the
    entire `model` object.

    :param model: A subclass of :class:`models.Model`

    """

    def __init__(self, model):
        self.model = model

    @nullable
    def validate(self, value):
        if not isinstance(value, self.model):
            raise errors.ValidationError(
                "should be an instance of '{}'".format(self.model.__name__))

        value.validate()


class Email(String):
    """This validator forces fields values to be strings and match a
    valid email address.

    """

    def __init__(self, *args, **kwargs):
        super(Email, self).__init__(*args, **kwargs)

        self.pattern = re.compile('^\w+\@\w+\.[a-z]{2,3}$')

    @nullable
    def validate(self, value):
        super(Email, self).validate(value)

        if self.pattern.match(value) is None:
            raise errors.ValidationError('should be a valid email')


class List(object):
    """This validator forces field values to be a :keyword:`list`.
    Also a list of inner :mod:`validators` could be specified to validate
    each list element. For example, to validate a list of
    :class:`models.Model` you could do::

        books = fields.Field(validators.List(validators.Model(YourBookModel)))

    :param \*validators: A list of inner validators as possitional arguments.

    """

    def __init__(self, *validators):
        self.validators = validators

    def validate(self, value):
        if not isinstance(value, list):
            raise errors.ValidationError('should be a list')

        for i in value:
            for validator in self.validators:
                validator.validate(i)
