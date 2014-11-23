Booby: data modeling and validation
===================================

.. image:: https://img.shields.io/pypi/v/booby.svg
    :target: https://pypi.python.org/pypi/booby
    :alt: Latest version

.. image:: https://readthedocs.org/projects/booby/badge
    :target: http://booby.readthedocs.org/en/latest
    :alt: Docs

.. image:: https://img.shields.io/badge/Licence-Apache2-brightgreen.svg
    :target: https://www.tldrlegal.com/l/apache2
    :alt: License

.. image:: https://img.shields.io/pypi/dm/booby.svg
    :target: https://pypi.python.org/pypi/booby
    :alt: Number of PyPI downloads

.. image:: https://secure.travis-ci.org/jaimegildesagredo/booby.svg?branch=master
    :target: http://travis-ci.org/jaimegildesagredo/booby
    :alt: Build status

Booby is a standalone data `modeling` and `validation` library written in Python. Booby is under active development (visit `this blog post <http://jaimegildesagredo.github.io/2014/01/04/booby-05-introducing-inspection-api.html>`_ for more info and the roadmap) and licensed under the `Apache2 license <http://www.apache.org/licenses/LICENSE-2.0.html>`_, so feel free to `contribute <https://github.com/jaimegildesagredo/booby/pulls>`_ and `report errors and suggestions <https://github.com/jaimegildesagredo/booby/issues>`_.

Usage
-----

See the sample code below to get an idea of the main features.

.. code-block:: python

    from booby import Model, fields


    class Token(Model):
        key = fields.String()
        secret = fields.String()


    class Address(Model):
        line_1 = fields.String()
        line_2 = fields.String()


    class User(Model):
        login = fields.String(required=True)
        name = fields.String()
        email = fields.Email()
        token = fields.Embedded(Token, required=True)
        addresses = fields.Collection(Address)

    jack = User(
        login='jack',
        name='Jack',
        email='jack@example.com',
        token={
            'key': 'vs7dfxxx',
            'secret': 'ds5ds4xxx'
        },
        addresses=[
            {'line_1': 'Main Street'},
            {'line_1': 'Main St'}
        ]
    )

    if jack.is_valid:
        print jack.to_json(indent=2)
    else:
        print json.dumps(dict(jack.validation_errors))

.. code-block:: json

    {
      "email": "jack@example.com",
      "login": "jack",
      "token": {
        "secret": "ds5ds4xxx",
        "key": "vs7dfxxx"
      },
      "name": "Jack",
      "addresses": [
        {
          "line_1": "Main St",
          "line_2": null
        },
        {
          "line_1": "Main Street",
          "line_2": null
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

    $ pip install -r test-requirements.txt
    $ nosetests tests/unit
    $ nosetests tests/integration

Changes
-------

See `Changes <https://booby.readthedocs.org/en/latest/changes.html>`_.
