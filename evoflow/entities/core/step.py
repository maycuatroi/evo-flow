import abc
import inspect
from copy import deepcopy
from functools import wraps

from evoflow.entities.core.base_object import BaseObject

from collections import OrderedDict


class Step(BaseObject):
    """
    Step is a cells of jobs
    """

    STATUS_PENDING = "pending"  # waiting to run
    STATUS_RUNNING = "running"  # running
    STATUS_SUCCESS = "success"  # success
    STATUS_FAILED = "failed"  # failed
    STATUS_SKIPPED = "skipped"  # skipped by condition
    STATUS_READY = "ready"  # ready to run

    def __call__(self, func) -> "Step":
        """

        :return: Step object
        :rtype: Step
        """

        def step_decorator(func):
            @wraps(func)
            def wrapper_action(*args: tuple, **kwargs: dict) -> "Step":
                """
                Wrapper method để tạo thành action trong step
                :param args:
                :param kwargs:
                :return:
                :rtype: Step
                """
                self.name = func.__name__.replace("_", " ").capitalize()
                params = inspect.getfullargspec(func)
                kwargs = {**kwargs, **dict(zip(list(params.args), args))}
                self.prepare(**kwargs)
                self.action = func
                return deepcopy(self)

            return wrapper_action

        return step_decorator(func)

    def __init__(self, name=None, transactions=None, **kwargs):
        """

        Args:
            name: Name of the step
            transactions: List of transactions
            **kwargs:
        """
        self.is_start = kwargs.get("is_start")
        self.is_end = kwargs.get("is_end")
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = transactions

        if name is None:
            name = self.__class__.__name__

        self.params = {"name": name}
        self.previous_steps = []
        self.error = None
        self.status = self.STATUS_PENDING
        self._job = None
        super().__init__(name=name, **kwargs)

    @property
    def job(self):
        return self._job

    @job.setter
    def job(self, value):
        self._job = value

    @abc.abstractmethod
    def action(self, **kwargs):
        """
        Performs the function of step
        """
        pass

    def set_error(self, error):
        self.status = self.STATUS_FAILED
        self.error = error

    def end(self, **kwargs) -> dict:
        """
        Kết thúc step, kill các object không cần thiết để giải phóng bộ nhớ
        """
        self.status = self.STATUS_SUCCESS
        self.job.remove_running_step(self)
        self.job.update_status()
        return self.params

    def prepare(self, **kwargs):
        """
        Chuẩn bị cho action, hàm prepare giúp chuẩn bị input để đẩy vào action()
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.params = kwargs
        self.job.add_running_step(self)
        self.status = self.STATUS_RUNNING
        self.job.update_status()

    def __str__(self):
        return self.name

    def get_next_steps(self, params=None):
        next_steps = []

        for transaction in self.transactions:
            if transaction.validate(**params):
                next_steps.append(transaction.to)

        return next_steps

    def next(self, to, condition="always"):
        from evoflow.entities.core.transaction import Transaction

        Transaction(step=self, to=to, condition=condition)
        return to

    def set_all_params(self, params):
        self.params = params

    # support '>>' operator
    def __rshift__(self, other):
        from evoflow.entities.core.step_list import StepList

        # connect to other step
        if isinstance(other, Step) or isinstance(other, StepList):
            return self.next(other)
        elif isinstance(other, list):
            return self.next(StepList(other))

    def __lshift__(self, other):
        from evoflow.entities.core.step_list import StepList

        # connect to other step
        if isinstance(other, Step) or isinstance(other, StepList):
            return other.next(self)
        elif isinstance(other, list):
            step_list = StepList(other)
            return step_list.next(self)
        raise Exception("Invalid step")

    def is_ready(self):
        """
        Check if step is ready to run
        """
        for step in self.previous_steps:
            if step.status != self.STATUS_SUCCESS:
                return False
            self.status = self.STATUS_READY
        return True

    def is_running(self):
        """
        Check if step is running
        """
        return self.status == self.STATUS_RUNNING
