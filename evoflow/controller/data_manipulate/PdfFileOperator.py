import pdfplumber

from evoflow.Controller.DataManipulate.FileOperator import FileOperator
from evoflow.Entities.DataManipulate.FileOperator.File import File
from evoflow.Entities.DataManipulate.FileOperator.PdfFile import PdfFile


class PdfFileOperator(FileOperator):
    """
    Read and write file PDF
    """

    def save(self, file: File, file_path) -> bool:
        pass

    def read(self, file_path, **args):
        file_data = pdfplumber.open(file_path)
        file = PdfFile(data=file_data, file_path=file_path)
        return file

    @staticmethod
    def supported_file_types():
        return ["pdf"]
