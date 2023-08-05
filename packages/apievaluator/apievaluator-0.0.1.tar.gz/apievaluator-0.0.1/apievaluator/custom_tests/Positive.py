from apievaluator.custom_tests import AbstractTest


class Positive(AbstractTest):

    def __init__(self, name: str):
        self.name = name

    def run(self, data: dict):
        val = data[self.name]

        if isinstance(val, (int, float)):
            return (val >= 0, 'OK - %s is positive' % self.name if val >= 0 else 'Expected positive number, got %d' % val)
        elif isinstance(val, str) and val.isnumeric():
            return (False, 'Expected a number, got numeric string')
        else:
            return (False, 'Expected a number, got %s' % type(val).__name__)
