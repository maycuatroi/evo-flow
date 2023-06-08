from evoflow.operators.base_operator import BaseOperator


class PythonOperator(BaseOperator):
    """
    Executes a Python callable
    """

    def __init__(self, python_callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.python_callable = python_callable

    def action(self, **kwargs):
        kwargs = {**kwargs, **self.op_kwargs}
        result = self.python_callable(*self.op_args, **kwargs)
        if isinstance(result, dict):
            kwargs = {**kwargs, **result}
        return kwargs
