Booby: data modeling and validation library
===========================================

Booby is a standalone data `modeling` and `validation` library written in Python. Booby is under active development and licensed under the `Apache2 license <http://www.apache.org/licenses/LICENSE-2.0.html>`_, so feel free to `contribute <https://github.com/jaimegildesagredo/booby/pulls>`_ and `report errors and suggestions <https://github.com/jaimegildesagredo/booby/issues>`_.

See the sample code below to get an idea of the main features::

    from booby import *

    class Token(Model):
        key = StringField()
        secret = StringField()

    class User(Model):
        login = StringField(required=True)
        name = StringField()
        email = StringField()
        token = EmbeddedField(Token, required=True)

    jack = User(
        login=u'jacko',
        name=u'Jack',
        email=u'jack@example.com',
        token={
            'key': u'vs7df...',
            'secret': u'ds5ds4...'
        }
    )

    try:
        jack.validate()
    except ValidationError:
        pass
    else:
        print jack.to_json()

Contents
--------

.. toctree::
    :maxdepth: 2

    models
    fields
    validators
    errors


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

