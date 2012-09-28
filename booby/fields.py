# -*- coding: utf-8 -*-


class Field(object):
    pass


class TypeField(Field):
    def __init__(self, **kwargs):
        self.name = None
        self.required = kwargs.get('required', False)

        try:
            choices = kwargs.get('choices', [])
            self.choices = set(self.validation(x) for x in choices)
        except ValueError:
            raise ValueError('Invalid choices: {0}'.format(choices))
        except TypeError:
            raise TypeError("'choices' is not iterable")

        try:
            default = kwargs.get('default')
            self.default = self.validation(default) if default is not None else default
        except ValueError:
            raise ValueError('Invalid default value: {0}'.format(default))

    def __get__(self, instance, owner):
        if instance is not None:
            return instance._data.get(self, self.default)
        return self

    def __set__(self, instance, value):
        instance._data[self] = self.validate(value)

    def validate(self, value):
        if value is None:
            if self.required:
                raise ValueError("Field '{0}' is required".format(self.name))
            return value

        if self.choices and value not in self.choices:
            raise ValueError("Invalid value for field '{0}': {1}".format(
                self.name, value))

        return self.validation(value)

    def validation(self, value):
        raise NotImplementedError()


class StringField(TypeField):
    def validation(self, value):
        if not isinstance(value, basestring):
            raise ValueError("Invalid value for field '{0}': {1}".format(
                self.name, value))
        return value


class IntegerField(TypeField):
    def validation(self, value):
        try:
            return int(value)
        except ValueError:
            raise ValueError("Invalid value for field '{0}': {1}".format(
                self.name, value))


class BoolField(TypeField):
    def validation(self, value):
        if not isinstance(value, (bool, int)):
            raise ValueError("Invalid value for field '{0}': {1}".format(
                self.name, value))
        return bool(value)
