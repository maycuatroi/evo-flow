import logging
import pathlib
import platform
import sys
import time

import coloredlogs

pathlib.Path("logs").mkdir(parents=True, exist_ok=True)
logger = logging.getLogger()
current_time_string = time.strftime("%Y%m%d-%H%M%S")
FILE_NAME = "logs/evoflow.log"
fh = logging.FileHandler(filename=FILE_NAME, mode="a", encoding="utf-8")
fh.setLevel(logging.ERROR)
formatter = coloredlogs.ColoredFormatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)
logger.addHandler(fh)
coloredlogs.install(level=logging.INFO, logger=logger)


def pretty_dict(dict_object, indent=0):
    pretty_string = "\n"
    for key, value in dict_object.items():
        pretty_string += "\t" * indent + str(key) + " : "
        pretty_string += "\t" * (indent + 1) + str(value) + "\n"
    return pretty_string


def get_os_information():
    os_information = """Python version: %s
    dist: %s
    system: %s
    machine: %s
    platform: %s
    uname: %s
    version: %s
    """ % (
        sys.version.split("\n"),
        str(platform.win32_edition()),
        platform.system(),
        platform.machine(),
        platform.platform(),
        platform.uname(),
        platform.version(),
    )

    return os_information
