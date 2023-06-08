import os

from evoflow import logger

try:
    from pywinauto import Application as App
except ImportError:
    logger.debug(
        "Can't import pywin32, try to install with:\nconda install pywin32\nOR\npip install pywin32==227"
    )

from evoflow.controller.log_controller import logger

DATA_PATH = "data"
START_CATIA = True


class Global:
    REMOTE_EXECUTE = False
    __caa = None
    custom_env = None
    ocr_engine = None

    def set_env(self, env):
        Global.custom_env = env
        return Global.custom_env

    @property
    def caa(self):
        if Global.__caa is None:
            try:
                logger.info("Opening CATIA Application ... ")
                if Global.custom_env is not None:
                    Global.__caa = start_catia(Global.custom_env)
                else:
                    Global.__caa = start_catia(None)
            except:
                logger.error("Can't start CATIA")
        return Global.__caa
