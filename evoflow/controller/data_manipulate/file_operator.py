#  Copyright (c) 2021. Copyright belongs to evoflow team

import abc

from tqdm import tqdm

from evoflow.Controller.DataManipulate.DataManipulate import DataManipulate
from evoflow.Entities.DataManipulate.FileOperator.File import File


def get_reader(file_type):
    """
    Trả về reader thỏa vãn mới file_type này
    """
    readers = FileOperator.__subclasses__()
    for reader in readers:
        if file_type in reader.supported_file_types():
            return reader()
    print(f"Can't read file with file type: .{file_type}")
    return None


def get_file_type(file_path):
    """
    Trả về file type của file_path
    """
    file_type = file_path.split(".")[-1].lower()
    return file_type


class FileOperator(DataManipulate):
    """
    Operator để thao tác xử lý files
    """

    def read(self, file_path, **args) -> File:
        """
        đọc file, tự lựa chọn cách đọc phù hợp cho các loại files
        :param file_path: đường dẫn tới file
        :args: Params bổ sung
        :return: Return None nếu đọc không thành công
        """

        file_type = get_file_type(file_path)
        reader = get_reader(file_type)
        return reader.read(file_path, **args)

    def reads(self, file_paths) -> list:
        """
        Đọc nhiều files khác nhau theo đường dẫn
        :param file_paths:  list file paths
        :return:
        """
        results = []
        for file_path in tqdm(file_paths, desc="Read files"):
            file_data = self.read(file_path)
            if file_data is not None:
                results.append(file_data)
        return results

    @abc.abstractmethod
    def save(self, file: File, file_path) -> bool:
        """
        Luư file
        :param file_path: Đường dẫn tới file
        :return:
        """

    def copy(self, file_source, file_destination, overwrite=False) -> str:
        """
        Coppy file from file_source to file_destination.
        :param overwrite: True thì ghi đè
        :param file_source: đường dẫn tới source file.
        :param file_destination:  đường dẫn nơi copy tới
        :return: Đường dẫn tới file sau khi Coppy
        """

    def remove(self, file_path, safe_delete=False) -> bool:
        """
            Xóa file tại đường dẫn file_path
            Nếu file_path là đường dẫn của folder thì xóa folder, nếu là file thì xóa file.

        :param file_path: đường dẫn tới file
        :param safe_delete: không xóa khi file đang được mở
        :return: True nếu xóa thành công
        """

    @staticmethod
    @abc.abstractmethod
    def supported_file_types():
        """
        trả về các loại file mà reader này hỗ trợ
        vd: ['xlsx','csv']
        """
        return []
