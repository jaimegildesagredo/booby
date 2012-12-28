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

from booby import validators as builtin_validators


class Field(object):
    def __init__(self, *validators, **kwargs):
        self.default = kwargs.get('default')

        # Setup field validators
        self.validators = []

        if kwargs.get('required'):
            self.validators.append(builtin_validators.Required())

        choices = kwargs.get('choices')

        if choices:
            self.validators.append(builtin_validators.In(choices))

        self.validators.extend(validators)

    def __get__(self, instance, owner):
        if instance is not None:
            return instance._data.get(self, self.default)
        return self

    def __set__(self, instance, value):
        instance._data[self] = value

    def validate(self, value):
        for validator in self.validators:
            validator.validate(value)


class StringField(Field):
    def __init__(self, *args, **kwargs):
        super(StringField, self).__init__(builtin_validators.String(), *args, **kwargs)


class IntegerField(Field):
    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(builtin_validators.Integer(), *args, **kwargs)


class FloatField(Field):
    def __init__(self, *args, **kwargs):
        super(FloatField, self).__init__(builtin_validators.Float(), *args, **kwargs)


class BooleanField(Field):
    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(builtin_validators.Boolean(), *args, **kwargs)


class EmbeddedField(Field):
    def __init__(self, model, *args, **kwargs):
        super(EmbeddedField, self).__init__(builtin_validators.Embedded(model),
            *args, **kwargs)

        self.model = model

    def __set__(self, instance, value):
        if isinstance(value, dict):
            value = self.model(**value)

        super(EmbeddedField, self).__set__(instance, value)
