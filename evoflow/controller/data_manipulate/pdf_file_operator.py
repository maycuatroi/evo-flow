import pdfplumber

from evoflow.controller.data_manipulate.file_operator import FileOperator
from evoflow.entities.data_manipulate.file_operator.file import File
from evoflow.entities.data_manipulate.file_operator.pdf_file import PdfFile


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
