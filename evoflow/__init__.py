import inspect
import os

os.environ["GIT_PYTHON_REFRESH"] = "quiet"
import sys

from evoflow import params
from evoflow import version as evoflow_version
from evoflow.controller.log_controller import logger

import git
from evoflow.entities.core.job import Job
from evoflow.entities.core.step import Step
from evoflow.__info__ import __website__

logger.debug(
    f"Start evoflow v {evoflow_version.__version__}. You can visit {__website__} for more information"
)

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


def init_setting():
    try:
        import setting

        for key in setting.__dict__:
            if str(key).startswith("__"):
                continue
            value = setting.__dict__[key]
            os.environ[key] = str(value)
    except Exception as e:
        logger.debug(e)
        logger.info("Can't import setting.py")


def versioning(version_module):
    try:
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        if version_module.__sha__ != sha:
            commits = list(repo.iter_commits("HEAD"))
            total_commit = len(commits)
            version_parts = version_module.__version__.split(".")
            version_parts[3] = str(total_commit)
            version_path = inspect.getfile(version_module)
            version_lines = [
                f"__version__ = '{'.'.join(version_parts)}'\n",
                f"__sha__ = '{sha}'",
            ]
            open(version_path, "w").writelines(version_lines)
    except:
        logger.error("Can't versioning")


def framework_versioning():
    versioning(evoflow_version)


def bot_versioning():
    try:
        import version

        versioning(version)
    except:
        logger.error("Can't versioning For Bot")


init_setting()
# framework_versioning()
bot_versioning()

IS_DEBUG = sys.gettrace() is not None
