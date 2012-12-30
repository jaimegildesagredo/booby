# Booby: data modeling and validation library [![Build Status](https://secure.travis-ci.org/jaimegildesagredo/booby.png)](http://travis-ci.org/jaimegildesagredo/booby)

Booby is a standalone data *modeling* and *validation* library written in Python. Booby is under active development and licensed under the [Apache2 license][apache], so feel free to [contribute][pulls] and [report errors and suggestions][issues].

See the sample code below to get an idea of the main features:

```python
from booby import *

class Token(Model):
    key = StringField()
    secret = StringField()

class User(Model):
    login = StringField(required=True)
    name = StringField()
    email = EmailField()
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
```

# Installation

You can install the last stable release of Booby from PyPI using pip or easy_install.

    $ pip install booby

Also you can install the latest sources from Github:

    $ pip install -e git+git://github.com/jaimegildesagredo/booby.git

# Tests

To run the Booby test suite you should install the development requirements and then run nosetests.

    $ pip install -r requirements-devel.txt
    $ nosetests tests/unit
    $ nosetests tests/integration

# Documentation

Booby docs are hosted on [Read The Docs][docs].


[apache]: http://www.apache.org/licenses/LICENSE-2.0.html
[pulls]: https://github.com/jaimegildesagredo/booby/pulls
[issues]: https://github.com/jaimegildesagredo/booby/issues
[docs]: https://booby.readthedocs.org
