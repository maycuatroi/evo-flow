import abc


class AbstractService:
    def __init__(self):
        pass

    @abc.abstractmethod
    def run(self, data, **args):
        pass

    @abc.abstractmethod
    def start(self, **args):
        pass

    @abc.abstractmethod
    def kill(self, **args):
        pass
