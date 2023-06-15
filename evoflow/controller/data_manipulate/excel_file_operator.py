#  Copyright (c) 2021. Copyright belongs to evoflow team

import pandas as pd

from evoflow.controller.data_manipulate.file_operator import FileOperator
from evoflow.entities.data_manipulate.file_operator.dataframe_file import DataFrameFile
from evoflow.entities.data_manipulate.file_operator.file import File


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
