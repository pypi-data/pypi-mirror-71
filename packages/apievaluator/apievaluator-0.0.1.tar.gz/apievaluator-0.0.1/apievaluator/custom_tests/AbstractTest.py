from abc import ABCMeta, abstractmethod


class AbstractTest(metaclass=ABCMeta):

    @abstractmethod
    def run(self, data: dict):
        pass
