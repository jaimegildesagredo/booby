Changes
=======

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
