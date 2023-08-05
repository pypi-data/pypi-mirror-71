from apievaluator.custom_tests import AbstractTest


class ObjectWithKeys(AbstractTest):

    def __init__(self, name: str, with_keys=[]):
        self.name = name
        self.with_keys = with_keys

    def run(self, data: dict):
        if isinstance(data[self.name], dict):

            prop = data[self.name]
            errors = []

            for key in self.with_keys:
                if key not in prop:
                    errors.append(key)

            if not errors:
                return (True, 'OK')
            else:
                return (False, 'Object is missing keys: %s' % errors)
        else:
            type = type(data[self.name]).__name__
            return (False, 'Property \'%s\' was of type %s, expected an object' % (self.name, type))
