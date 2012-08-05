# -*- coding: utf-8 -*-


class Field(object):
    def __init__(self, **kwargs):
        self.name = None
        self.required = kwargs.get('required', False)

        try:
            choices = kwargs.get('choices', [])
            self.choices = set(self.validate(x) for x in choices)
        except ValueError:
            raise ValueError('Invalid choices: {0}'.format(choices))
        except TypeError:
            raise TypeError("'choices' is not iterable")

        default = kwargs.get('default')
        try:
            self.default = self.validate(default) if default is not None else default
        except ValueError:
            raise ValueError('Invalid default value: {0}'.format(default))

    def __get__(self, instance, owner):
        if instance is not None:
            return instance._data.get(self, self.default)
        return self

    def __set__(self, instance, value):
        instance._data[self] = self._validate(value)

    def _validate(self, value):
        if value is None:
            if self.required:
                raise ValueError("Field '{0}' is required".format(self.name))
            return value

        if self.choices and value not in self.choices:
            raise ValueError("Invalid value for field '{0}': {1}".format(
                self.name, value))

        return self.validate(value)

    def validate(self, value):
        raise NotImplementedError()


class StringField(Field):
    def validate(self, value):
        if not isinstance(value, basestring):
            raise ValueError("Invalid value for field '{0}': {1}".format(
                self.name, value))
        return value
