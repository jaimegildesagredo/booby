.. Booby documentation master file, created by
   sphinx-quickstart on Fri Dec 28 14:02:27 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Booby's documentation!
=================================

Booby is a standalone data modeling and validation Python library.

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

Contents:

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

