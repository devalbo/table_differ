__author__ = 'ajb'

# import jsonpickle
import json

class Abc(object):

    def __init__(self):
        self._to_pickle = None

    def set_to_pickle(self, value):
        self._to_pickle = value


abc = Abc()
d = {
    (1, 2): 'abc',
    (0,0): 'def',
    }
abc.set_to_pickle(d)

print json.dumps(abc)
