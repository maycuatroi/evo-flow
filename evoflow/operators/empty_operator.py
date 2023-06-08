from evoflow.operators.base_operator import BaseOperator


class EmptyOperator(BaseOperator):
    """
    Executes a Python callable
    :param python_callable: A reference to an object that is callable
    :type python_callable: python callable
    :param op_args: a list of positional arguments to pass to python_callable
    :type op_args: list
    :param op_kwargs: a dict of keyword arguments to pass to python_callable
    :type op_kwargs: dict
    :param templates_dict: a dictionary of templates variables to pass to python_callable
    :type templates_dict: dict
    :param templates_exts: a list of file extensions to resolve templates
    :type templates_exts: list
    """

    template_fields = ("templates_dict", "op_args", "op_kwargs")
    template_ext = tuple()
    ui_color = "#ffefeb"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
