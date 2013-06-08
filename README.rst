Booby: data modeling and validation library
===========================================

.. image:: https://secure.travis-ci.org/jaimegildesagredo/booby.png?branch=master
    :target: http://travis-ci.org/jaimegildesagredo/booby

Booby is a standalone data `modeling` and `validation` library written in Python. Booby is under active development and licensed under the `Apache2 license <http://www.apache.org/licenses/LICENSE-2.0.html>`_, so feel free to `contribute <https://github.com/jaimegildesagredo/booby/pulls>`_ and `report errors and suggestions <https://github.com/jaimegildesagredo/booby/issues>`_.

See the sample code below to get an idea of the main features.

.. code-block:: python

    from booby import *

    class Token(Model):
        key = StringField()
        secret = StringField()

    class Address(Model):
        line_1 = StringField(required=True)
        line_2 = StringField()
        city = StringField(choices=[ ... ])
        state = StringField(choices=[ ... ])
        zip_code = StringField()

    class User(Model):
        login = StringField(required=True)
        name = StringField()
        email = EmailField()
        token = EmbeddedField(Token, required=True)
        addresses = Field(validators.List(validators.Model(Address)), default=[])

    jack = User(
        login=u'jack',
        name=u'Jack',
        email=u'jack@example.com',
        token={
            'key': u'vs7df...',
            'secret': u'ds5ds4...'
        },
        addresses=[
            Address(line_1='foo', ...),
            Address(line_1='bar', ...)
        ]
    )

    try:
        jack.validate()
    except ValidationError as error:
        print error
    else:
        print jack.to_json(indent=2)

    {
      "email": "jack@example.com",
      "login": "jack",
      "token": {
        "secret": "ds5ds4...",
        "key": "vs7df..."
      },
      "name": "Jack",
      "addresses": [
        {
          "line_1": "foo",
          "line_2": "..."
        },
        {
          "line_1": "bar",
          "line_2": "..."
        }
      ]
    }

Installation
------------

You can install the last stable release of Booby from PyPI using pip or easy_install.

.. code-block:: bash

    $ pip install booby

Also you can install the latest sources from Github.

.. code-block:: bash

    $ pip install -e git+git://github.com/jaimegildesagredo/booby.git#egg=booby

Tests
-----

To run the Booby test suite you should install the development requirements and then run nosetests.

.. code-block:: bash

    $ pip install -r requirements-devel.txt
    $ nosetests tests/unit
    $ nosetests tests/integration

Documentation
-------------

Booby docs are hosted on `Read The Docs <https://booby.readthedocs.org>`_.
