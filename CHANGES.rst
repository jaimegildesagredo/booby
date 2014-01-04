Changes
=======

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
