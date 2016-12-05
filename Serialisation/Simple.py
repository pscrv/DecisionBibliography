import json

REGISTRY = {}

def serialisable(cls):
    class wrapper:                

        def __init__(self, *args):
            self._class = cls
            self._serialisationargs = args
            REGISTRY[cls.__name__] = cls             
            self._wrapped = cls(*args)

        def __getattr__(self, *args):
            return getattr(self._wrapped, *args)

        def __repr__(self):
            return self._wrapped.__repr__()

        def __eq__(self, other):
            if isinstance(other, wrapper):
                return self._wrapped.__eq__(other._wrapped)
            return self._wrapped.__eq__(other)

        def __hash__(self):
            return self._wrapped.__hash__()

        def serialise(self):
            jsondictionary = {
                'class': self._class.__name__,
                'args': self._serialisationargs,
                }
            return json.dumps(jsondictionary)

    return wrapper

def deserialise(jsonstring):
    jsondictionary = json.loads(jsonstring)
    classname = jsondictionary['class']
    makeargs = jsondictionary['args']
    return REGISTRY[classname](*makeargs)


