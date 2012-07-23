# -*- coding: utf-8 -*-

import json

from lettuce import step, world

from booby import Model, StringField


@step(u'I have an User model')
def i_have_an_user_model(step):
    @world.absorb
    class User(Model):
        name = StringField()
        email = StringField()


@step(u'create an User instance with the user')
def create_an_user_instance_with_user_the_data(step):
    world.user = world.User(name=u'Foo', email=u'foo@example.com')


@step(u'I dump the object using the json module')
def i_dump_the_object_using_the_json_module(step):
    world.json = json.dumps(dict(world.user))


@step(u'I get a string with the json')
def i_get_a_string_with_the_json(step):
    json_user = json.loads(world.json)

    assert json_user['name'] == world.user.name
    assert json_user['email'] == world.user.email