from pptx import Presentation

from evoflow.controller.data_manipulate.file_operator import FileOperator
from evoflow.entities.data_manipulate.file_operator.file import File
from evoflow.entities.data_manipulate.file_operator.pptx_file import PPTXFile


class PptxFileOperator(FileOperator):
    def save(self, file: File, file_path) -> bool:
        file.data: Presentation
        file.data.save(file_path)
        return True

    def read(self, file_path, **args):
        file = PPTXFile(file_path=file_path)
        file.data = Presentation(file_path)
        return file

    @staticmethod
    def supported_file_types():
        return ["ppt", "pptx"]
