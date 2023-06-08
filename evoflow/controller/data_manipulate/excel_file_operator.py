#  Copyright (c) 2021. Copyright belongs to evoflow team

import pandas as pd

from evoflow.controller.data_manipulate.FileOperator import FileOperator
from evoflow.Entities.DataManipulate.FileOperator.DataFrameFile import DataFrameFile
from evoflow.Entities.DataManipulate.FileOperator.File import File


class ExcelFileOperator(FileOperator):
    def read(self, file_path, **args) -> File:
        """
        read file excel
        :param file_path:
        :return:
        """

        file = DataFrameFile(file_path=file_path)
        file.data = pd.read_excel(file_path, **args)
        return file

    def save(self, file: File, file_path) -> bool:
        """
        save excel file
        :param file:
        :param file_path:
        :return:
        """
        file.data: pd.DataFrame
        file.data.to_excel(file_path)
        return file_path

    @staticmethod
    def supported_file_types():
        return ["xlsx", "csv", "xls"]
