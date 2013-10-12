# -*- coding: utf-8 -*-
#
# Copyright 2013 Jaime Gil de Sagredo Luna
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

"""The :mod:`inspection` module provides users and 3rd-party libraries
developers a public api to access :class:`models.Model` objects and
subclasses info, such the `model` defined fields.

"""

from booby import models, errors


def inspect(model):
    """Returns a :class:`ModelInspector` object for the given
    `model` :class:`models.Model` instance or subclass.

    If given `model` is not a :class:`models.Model` instance nor subclass
    then raises :class:`errors.InspectError`.

    """

    if isinstance(model, models.Model) or issubclass(model, models.Model):
        return ModelInspector(model)

    raise errors.InspectError(
        'Expected a {} instance or subclass'.format(models.Model))


class ModelInspector(object):
    """The :class:`ModelInspector` class is used to access a
    :class:`models.Model` object info.

    This class shouldn't be instantiated directly, instead the
    :func:`inspect` function should be used.

    """

    def __init__(self, model):
        self._model = model

    @property
    def fields(self):
        """This property contains a dict mapping field names and field
        objects.

        """

        return self._model._fields
