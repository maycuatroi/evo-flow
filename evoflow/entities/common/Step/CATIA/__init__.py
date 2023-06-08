import evoflow
from evoflow.Controller.DataManipulate.FileOperator import FileOperator

@evoflow.Step()
def open_catia_file(path: str = None):
    FileOperator().read(path)
