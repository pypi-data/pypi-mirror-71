import re

from apievaluator.custom_tests import AbstractTest


class StringRegex(AbstractTest):

    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = regex

    def run(self, data: dict):
        match = re.search(self.regex, data[self.name])

        if match:
            return (True, 'OK - regex %s matched' % self.regex)
        else:
            return (False, 'Regex %s failed for string %s' % (self.regex, data[self.name]))
