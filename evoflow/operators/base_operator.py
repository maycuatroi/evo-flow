from evoflow import Step


class BaseOperator(Step):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_id = kwargs.get("task_id", None)
        self.name = self.task_id

    def __str__(self):
        return f"{self.__class__.__name__} {self.task_id}"

    def __repr__(self):
        return f"{self.__class__.__name__} {self.task_id}"
