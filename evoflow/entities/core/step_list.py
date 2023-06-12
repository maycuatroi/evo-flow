import typing
from concurrent.futures import ThreadPoolExecutor
from evoflow.entities.core.step import Step


class StepList(Step):
    def __init__(self, steps=None, transactions=None, **kwargs):
        super().__init__(**kwargs)
        self.steps = steps or []
        self.transactions = transactions or []

    def add_step(self, step: "Step"):
        self.steps.append(step)

    def __rshift__(self, other):
        """
        @param other: Step
        @return:

        """
        from evoflow.entities.core.step import Step

        if isinstance(other, Step):
            return self.next(other)
        raise TypeError(f"StepList can't connect to {type(other)}")

    def next(self, to: typing.Union["Step", "StepList"], condition="always"):
        from evoflow.entities.core.transaction import Transaction

        Transaction(step=self, to=to, condition=condition)

        return to

    def __repr__(self):
        return f"StepList: {self.steps}"

    def __str__(self):
        return f"StepList: {self.steps}"

    def __getitem__(self, item):
        return self.steps[item]

    def action_sub_step(self, step: Step, **kwargs):
        """
        Performs the function of step
        """
        kwargs = {**self.params, **kwargs}
        step.prepare(**kwargs)
        step.action(**kwargs)
        step.end(**kwargs)

    def action(self, **kwargs):
        """
        Performs the function of step
        """
        kwargs = {**self.params, **kwargs}
        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(lambda step: self.action_sub_step(step, **kwargs), self.steps))

    def get_remaining_step(self):
        return [step for step in self.steps if not step.is_running()]

    @property
    def job(self):
        return super().job

    @job.setter
    def job(self, value):
        self._job = value
        for step in self.steps:
            step.job = value
