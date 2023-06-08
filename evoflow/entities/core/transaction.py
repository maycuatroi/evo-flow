from evoflow import logger
from evoflow.entities.core.base_object import BaseObject
from evoflow.entities.core.condition import Condition
from evoflow.entities.core.step import Step


class Transaction(BaseObject):
    def __init__(self, step: Step, to: Step, condition="always"):
        self.id = str(step.id) + "-" + str(to.id)
        self.to = to
        self.__from_step__ = step
        self.condition = Condition(condition)
        self.__from_step__.transactions.append(self)

    def validate(self, **kwargs):
        if type(self.condition.condition_function) == str:
            if self.condition.condition_function == "always":
                return True
            return self.build_condition_from_string(
                self.condition.condition_function, self.__from_step__.params
            )
        return bool(self.condition.condition_function(**kwargs))

    def build_condition_from_string(self, condition_function_string, params):
        """
        @param condition_function_string: Ex - select_condition == 3
        @return:
        """
        for k, v in params.items():
            try:
                exec(f"{k} = {v}\n")
            except Exception as e:
                logger.debug(
                    f"{e}\nCan't build param {k} to create condition from string, try to create condition with lambda function"
                )
        exec("global result\nresult = %s" % (condition_function_string))
        global result
        return result

    def to_dict(self):
        data = {
            "id": self.id,
            "from": self.__from_step__.id,
            "to": self.to.id,
            "condition": self.condition,
        }

        return data
