import importlib
import inspect
import json
import os
import sys

from tqdm import tqdm

from evoflow.controller.log_controller import logger, pretty_dict
from evoflow.entities.core.base_object import BaseObject
from evoflow.entities.core.step import Step
from evoflow.entities.core.transaction import Transaction


class Job(BaseObject):
    """
    Job : Các bot sẽ được tạo dưới dạng các Job.

    Example:
        job = Job(name='#323', steps=[
            ReadConfigFile(config_file_path='config/process_a1_config.xlsx'),
            PrepareInput(),
            RemoveUnusedPart(),
            GetDistanceThreshold(),
            MainProcess(),
            ShowHideForCapture(),
            Capture(),
            SaveOutput(),
        ])

        job.run() # run bot
        job.package('bots') # package bot

    """

    def __info__(self, **kwargs) -> dict:
        info = f"Job {self.name}"
        return info

    def kill(self, **kwargs):
        pass

    def finish(self, **kwargs):
        logger.info(f"Finish job: {self.name}")

    def __step_generator(self):
        self.stacks = [self.start_step]
        while len(self.stacks) > 0:
            step_i = self.stacks.pop()
            self.current_step = step_i
            yield step_i

    def run(self, **kwargs):
        logger.info(f"Running job: {self.name}")
        self.params_pool = kwargs
        step_generator = self.__step_generator()

        for step in tqdm(step_generator, unit="step"):
            log_string = f"Running step : {step.name}"
            logger.info(log_string)

            step.prepare(**self.params_pool)
            try:
                action_params = inspect.getfullargspec(step.action).args
                build_params = {}
                for param in action_params:
                    if param == "self":
                        continue
                    build_params[param] = step.__dict__.get(param)
                last_result = step.action(**build_params)
            except AttributeError:
                logger.error(f"Current Job params: {pretty_dict(self.params_pool)}")
                raise
            step.end(**kwargs)

            if last_result is not None:
                self.params_pool = {**self.params_pool, **last_result}
            step.set_all_params(self.params_pool)
            self.stacks += step.get_next_steps(self.params_pool)

        self.finish()

        return last_result

    def __init__(self, name=None, start_step: Step = None, **kwargs):
        self.current_step = None
        self.__start_step = start_step
        self.params_pool = {}
        if name is None:
            name = os.getenv("JOB_NAME")
        super().__init__(name=name, **kwargs)

    @property
    def start_step(self):
        return self.__start_step

    @start_step.setter
    def start_step(self, value):
        self.__start_step = value
        self.__start_step.is_start = True

    def document(self):
        pass

    def show_graph(self):
        pass

    def get_all_steps(self):
        steps = [self.start_step]
        queues = [self.start_step]
        while queues:
            step = queues.pop()
            transactions = step.transactions
            for transaction in transactions:
                transaction: Transaction
                next_step = transaction.to
                if next_step not in steps:
                    steps.append(next_step)
                    queues.append(next_step)
        return steps

    def to_nodered_id(self, id):
        return id[:8] + "." + id[8:13]

    def to_json(self):
        # jsonStr = json.dumps(obj.__dict__)
        steps = [self.start_step]
        steps.extend(self.get_all_steps())
        steps_dict = [
            {
                "id": "7027fc3.86fe004",
                "type": "tab",
                "label": "Flow 1",
                "disabled": False,
                "info": "",
            }
        ]
        for i in range(len(steps)):
            step_dict = {}
            step_dict["id"] = self.to_nodered_id(steps[i].id)
            step_dict["type"] = "step"
            step_dict["z"] = "7027fc3.86fe004"
            step_dict["name"] = "Step" + str(i + 1)
            params_dict = {}
            params = inspect.getfullargspec(steps[i].action).args
            for param in params:
                params_dict[param] = steps[i].__dict__.get(param)
            step_dict["params"] = params_dict
            condition = ""
            for step in steps:
                if steps[i] == step:
                    continue
                for transaction in step.transactions:
                    if transaction.to.id == steps[i].id:
                        condition = transaction.condition.condition_function
                    break
            step_dict["condition"] = condition
            step_dict["conditionFormat"] = "string"
            step_dict["stepType"] = steps[i].action.__name__
            step_dict["x"] = 100
            step_dict["y"] = 50 + i * 50
            # get transactions
            transactions_dict = []
            for transaction in steps[i].transactions:
                transactions_dict.append(self.to_nodered_id(transaction.to.id))
            step_dict["wires"] = transactions_dict
            steps_dict.append(step_dict)
        return json.dumps(steps_dict, ensure_ascii=False, indent=4)

    @staticmethod
    def load_job(path: str):
        base_path, module = os.path.split(path)
        sys.path.append(base_path)
        job = importlib.import_module(f"{module}.main").job
        return job

    def __call__(self, original_function):
        def wrapper_job(*args, **kwargs):
            step = Step(*args, **kwargs)
            step.action = original_function
            self.start_step = step
            return self

        return wrapper_job

    def to_dict(self):
        steps = self.get_all_steps()
        data = {"name": self.name, "id": self.id}
        data["steps"] = []
        for step in steps:
            step: Step
            data["steps"].append(step.to_dict())

        return data

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.finish()
