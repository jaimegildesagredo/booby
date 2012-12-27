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

"""Field validators"""

from booby import errors


class Required(object):
    def validate(self, value):
        if value is None:
            raise errors.ValidationError('is required')


class In(object):
    def __init__(self, choices):
        self.choices = choices

    def validate(self, value):
        if value not in self.choices:
            raise errors.ValidationError('should be in {}'.format(self.choices))


class String(object):
    def validate(self, value):
        if value is not None and not isinstance(value, basestring):
            raise errors.ValidationError('should be a string')


class Integer(object):
    def validate(self, value):
        if value is not None and not isinstance(value, int):
            raise errors.ValidationError('should be an integer')


class Float(object):
    def validate(self, value):
        if value is not None and not isinstance(value, float):
            raise errors.ValidationError('should be a float')


class Boolean(object):
    def validate(self, value):
        if value is not None and not isinstance(value, bool):
            raise errors.ValidationError('should be a boolean')


class Embedded(object):
    def __init__(self, model):
        self.model = model

    def validate(self, value):
        if value is None:
            return

        if not isinstance(value, self.model):
            raise errors.ValidationError(
                "should be an instance of '{}'".format(self.model.__name__))

        value.validate()
