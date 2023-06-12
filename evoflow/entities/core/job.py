import importlib
import inspect
import json
import os
import sys
import typing
from time import sleep

from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress
from rich.spinner import Spinner
from rich.text import Text
from rich.tree import Tree
from tqdm import tqdm

from evoflow.controller.log_controller import logger, pretty_dict
from evoflow.entities.core.base_object import BaseObject
from evoflow.entities.core.step import Step
from evoflow.entities.core.step_list import StepList
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

    def __step_generator(self) -> typing.Generator:
        self.stacks = self.get_all_steps()
        while len(self.stacks) > 0:
            for i, step in enumerate(self.stacks):
                if step.is_ready():
                    self.current_step = step
                    self.stacks.pop(i)
                    yield step
            sleep(0.1)

    def run(self, **kwargs):
        with Live(
            Panel(Columns([]), title=f"Running {self.name}"),
            refresh_per_second=20,
        ) as live:
            # live.update(Panel(spinners, title="Panel 2"))

            self.live_panel = live
            while True:
                # do self.__run by new thread
                self.__run(live=live, **kwargs)

    def __run(self, **kwargs):
        self.compile()
        logger.info(f"Running job: {self.name}")
        self.params_pool = kwargs
        step_generator = self.__step_generator()

        for step in step_generator:
            log_string = f"Running step : {step}"
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
            except AttributeError as e:
                logger.error(f"Current Job params: {pretty_dict(self.params_pool)}")
                step.set_error(e)
                raise
            step.end(**kwargs)

            if last_result is not None:
                self.params_pool = {**self.params_pool, **last_result}
            step.set_all_params(self.params_pool)

        self.finish()
        return last_result

    def __init__(self, name=None, start_step: Step = None, **kwargs):
        self.live_panel = None  # for progress monitor
        self.current_step = None
        self.__start_step: Step = start_step
        self.params_pool = {}
        self.__steps = []
        self.__running_steps = []
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

    def find_previous_steps(self, step, all_steps):
        previous_steps = []
        for step_i in all_steps:
            if step in step_i.get_next_steps():
                previous_steps.append(step_i)
        return previous_steps

    def compile(self):
        self.__steps = self.get_all_steps()
        for step in self.__steps:
            step.job = self

    def add_running_step(self, step):
        self.__running_steps.append(step)

    def remove_running_step(self, step):
        self.__running_steps.remove(step)

    def update_status(self, **kwargs):
        if self.live_panel is None:
            return
        tree = Tree(self.name)
        running_steps = self.__running_steps

        tree_added_steps = []

        step_lists = [_ for _ in running_steps if isinstance(_, StepList)]
        single_steps = [_ for _ in running_steps if not isinstance(_, Step)]

        for step_list in step_lists:
            remaining_steps = len(step_list.get_remaining_step())
            total_step = len(step_list.steps)
            step_title = f"{step_list.name} {total_step-remaining_steps}/{total_step}"

            spinner = Spinner("material", text=Text(step_title, style="green"))
            step_live = tree.add(spinner)
            for sub_step in step_list.steps:
                if sub_step.is_running():
                    step_live.add(Spinner("material", text=Text(sub_step.name, style="blue")))
                    tree_added_steps.append(sub_step)
        for step in single_steps:
            if step in tree_added_steps:
                continue
            if step.is_running():
                tree.add(Spinner("material", text=Text(step.name, style="blue")))

        self.live_panel.update(Panel(tree, title=f"Running {self.name}"))
