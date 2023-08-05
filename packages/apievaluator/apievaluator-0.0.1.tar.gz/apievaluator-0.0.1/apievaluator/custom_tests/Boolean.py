from apievaluator.custom_tests import AbstractTest


class Boolean(AbstractTest):

    def __init__(self, name: str, should_be: bool):
        self.name = name
        self.should_be = should_be

    def run(self, data: dict):
        res = data[self.name] == self.should_be
        return (res, 'OK' if res else 'Property %s was %s instead of %s' % (self.name, data[self.name], self.should_be))
