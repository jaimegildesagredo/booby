# -*- coding: utf-8 -*-
#
# Copyright 2014 Jaime Gil de Sagredo Luna
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

import collections

from booby import mixins, errors


class Model(object):
    def __call__(self, value):
        if value is None:
            return

        return value.encode()


class List(object):
    def __call__(self, value):
        if value is None:
            return

        if not isinstance(value, collections.MutableSequence):
            raise errors.EncodeError()

        return [item.encode() if isinstance(item, mixins.Encoder) else item
                for item in value]


class DateTime(object):
    def __init__(self, format=None):
        self._format = format

    def __call__(self, value):
        if value is None:
            return

        if self._format is None:
            return value.isoformat()

        return value.strftime(self._format)
