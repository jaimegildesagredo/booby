Changes
=======

0.7.1 (Aug 26, 2016)
--------------------

* Added new type: URL.
* Added new property to fields: Description.
* Added the optional use os UstraJSON, ultra fast JSON serializer.
* Added 'properties' classmethod to Models. With it, you can get the fields defined in a Model, without instantiate it.
* Improved validation. Now, types derived from basic types has strong checks: int, fload, bool, string, list.
* Improved compatibility with Python 3.


0.7.0 (Dec 3, 2014)
-------------------

Backwards-incompatible
^^^^^^^^^^^^^^^^^^^^^^

* The ``List`` encoder no longers encodes models. To achieve the old behavior pass the ``Model`` encoder as an argument instead::

    class User(Model):
        tokens = fields.Field(encoders=[encoders.List(encoders.Model())])

Highlights
^^^^^^^^^^

* Added a ``Collection`` field that works like ``Embedded`` for lists of models::

    class User(Model):
        tokens = fields.Collection(Token)

    user = User({
        'tokens': [
            {
                'key': 'xxx',
                'secret': 'yyy'
            }
        ]
    })

    user.tokens.append(Token(key='zzz', secret='www'))
    user.validate()

See `the docs <http://booby.readthedocs.org/en/latest/fields.html#fields.Collection>`_ for more info.

0.6.0 (Oct 12, 2014)
--------------------

Backwards-incompatible
^^^^^^^^^^^^^^^^^^^^^^

* The `List` validator now accepts `None` as a valid value allowing not required list fields. Before this a field with a `List` validator couldn't be `None`.

Highlights
^^^^^^^^^^

* The `Model` class now defines a `decode` and `encode` methods with serialization/deserialization support.
* A `Field` now can receive lists of callable objects, `encoders` and `decoders`, to perform serialization/deserialization.
* Added a `List` field that can be used to create fields containing lists of objects (even models).
* Datetime validator, encoder, and decoder were added.

0.5.2 (Mar 22, 2014)
--------------------

Highlights
^^^^^^^^^^

* Added readable `Field` instances repr. See `issue 20 <https://github.com/jaimegildesagredo/booby/issues/20>`_.
* Added readable `Model` classes and instances repr.

0.5.1 (Jan 31, 2014)
--------------------

Highlights
^^^^^^^^^^

* The `Email` validator now only performs a basic sanity check instead of the more restrictive previous check. See `issue 17 <https://github.com/jaimegildesagredo/booby/issues/17>`_.
* The `List` validator now accepts any object that implements the `list` interface (collections.MutableSequence). See `issue 18 <https://github.com/jaimegildesagredo/booby/issues/18>`_.
* Any object implementing the `dict` interface (collections.MutableMapping) can be used as a value for an `Embedded` field. See `issue 18 <https://github.com/jaimegildesagredo/booby/issues/18>`_.
* When iterating a `Model` object all objects implementing the `list` interface are treated as lists. See `issue 18 <https://github.com/jaimegildesagredo/booby/issues/18>`_.

0.5.0 (Jan 4, 2014)
-------------------

Backwards-incompatible
^^^^^^^^^^^^^^^^^^^^^^

* Now field `validators` must be callable objects. Before this release validators had a `validate` method that is not longer used to perform a validation. This change only affects to custom user validators with a `validate` method.

Highlights
^^^^^^^^^^

* The `FieldError` exception now is raised only with the field name as argument. See `issue 12 <https://github.com/jaimegildesagredo/booby/issues/12>`_.
* Fields `default` argument callables can now optionally receive the model as argument.
* Added the `inspection` module which provides the `get_fields` and `is_model` functions as a public api to get access to `models` fields and type validation.

0.4.0 (Ago 4, 2013)
-------------------

Backwards-incompatible
^^^^^^^^^^^^^^^^^^^^^^

* Moved the `Model.to_dict` functionality to `dict(model)`.
* The `Model.validation_errors` method now is an interable of field name and validaton error pairs.
* Removed the `Field` subfix for all Booby fields. Now use the module as namespace: `fields.String`.

Highlights
^^^^^^^^^^

* Added an `is_valid` property to `Model`.
* The `Model` instances now are iterables of field name, value pairs.

0.3.0 (Jun 20, 2013)
--------------------

Highlights
^^^^^^^^^^

* When passed a `callable` object as a field `default` then the default value for this field in a model instance will be the return value of the given callable.

* Added the :func:`models.Model.validation_errors` method to get a dict of field name and error message pairs for all invalid model fields.
