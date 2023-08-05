from apievaluator.custom_tests import AbstractTest


class ArrayOfLength(AbstractTest):

    def __init__(self, name: str, len: int):
        self.name = name
        self.len = len

    def run(self, data: dict):
        val = data[self.name]

        if isinstance(val, list):
            if len(val) == self.len:
                return (True, 'OK')
            else:
                return (False, '%s is of length %d, expected %d', self.name, len(val), self.len)
        else:
            return (False, '%s is not an array, got %s instead', self.name, type(val).__name__)
