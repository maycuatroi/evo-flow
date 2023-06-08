from evoflow import Step


class BaseOperator(Step):
    def __init__(self, op_args=None, op_kwargs=None, **kwargs):
        super().__init__(**kwargs)
        self.task_id = kwargs.get("task_id", None)
        self.name = self.task_id
        self.op_args = op_args or []
        self.__op_kwargs = op_kwargs or {}

    @property
    def op_kwargs(self):
        return {**self.__op_kwargs, **{"ti": self}}

    def __str__(self):
        return f"{self.__class__.__name__} {self.task_id}"

    def __repr__(self):
        return f"{self.__class__.__name__} {self.task_id}"

    def xcom_push(self, key, value):
        self.params[key] = value

    def xcom_pull(self, key, **kwargs):
        return self.params[key]