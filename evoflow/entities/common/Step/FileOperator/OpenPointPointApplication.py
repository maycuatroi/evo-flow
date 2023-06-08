import subprocess

from evoflow.Entities.Core.Step import Step


class OpenPointPointApplication(Step):
    """
    Open PowerPoint File

    """

    def __init__(self, **kwargs):
        """

        @param file_path: path of powerpoint file
        """

    def action(self):
        subprocess.Popen(r'"C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE" ' + f'"{self.file_path}"')
