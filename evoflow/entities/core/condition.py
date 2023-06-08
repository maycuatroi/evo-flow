import inspect

from evoflow.entities.core.base_object import BaseObject


class Condition(BaseObject):
    def __init__(self, condition_function):
        """

        @param condition_function: Boolean Validate function
        """
        self.condition_function = condition_function

    def to_dict(self):
        if type(self.condition_function) != str:
            args = inspect.getfullargspec(self.condition_function).args
            z = inspect.getsource(self.condition_function)
            return {"condition_function": {"args": args, "source": z}}
        return self.__dict__
