"""The `serialize` module contains the `booby` functions to serialize, deserialize
collection of `Model` objects

Something like this::

    class Repo(Model):
         name = fields.String()
         owner = fields.Embedded(User)

    objects = [Repo(
                   name='Booby',
                   owner={
                       'login': 'jaimegildesagredo',
                       'name': 'Jaime Gil de Sagredo'
                   }),
               Repo(
                   name='Booby2',
                   owner={
                       'login': 'what ever',
                       'name': 'who cares'
                   })
               ]

    serialize(objects, out_file=my_open_file)
    deserialize(my_json_file)
"""
import json
from booby.errors import SerializationError, DeSerializationError
from booby.models import Model
from importlib import import_module


def _serialize(obj):
    '''returns model object as dict if it is valid
    '''
    if obj.is_valid and obj._meta['allow_serialize']:
        return obj.to_dict()
    else:
        raise SerializationError("{0} is not serializable".format(repr(obj)))


def serialize(objects, out_file=None, *args, **kwargs):

    if isinstance(objects, Model):
        objects = [objects]

    if out_file:
        return json.dump(map(_serialize, objects), out_file, *args, **kwargs)
    else:
        return json.dumps(map(_serialize, objects), *args, **kwargs)


def _deserialize(dct):
    try:
        if "model" not in dct:
            raise DeSerializationError("json object has no attribute `model`")

        model = dct["model"]
        data = dct["obj"]

        _module, dot, _class = model.rpartition('.')
        cls = getattr(import_module(_module), _class)

        _object = cls(**data)
        if not _object.is_valid:
            raise DeSerializationError("json object is not a valid {0} instance".
                                     format(model))
        else:
            return _object

    except ImportError:
        raise DeSerializationError("can not import your model{0}".format(model))


def deserialize(json_data, *args, **kwargs):

    if hasattr(json_data, 'read'):
        data = json.load(json_data)
    else:
        data = json.loads(json_data)

    if not isinstance(data, list):
        data = [data]

    objects = []
    for dct in data:
        objects.append(_deserialize(dct))
    return objects
