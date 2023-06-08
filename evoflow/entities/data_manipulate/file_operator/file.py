import os
from abc import abstractmethod

from evoflow.entities.data_manipulate.abstract_data import AbstractData


class File(AbstractData):
    def __init__(self, file_path: str = None, **args):
        self.file_path = file_path

        self.file_name = os.path.split(file_path)[1].replace(
            "." + self.get_file_type(), ""
        )
        self.data = args.get("data")
        self.__meta_data__ = None
        super().__init__()

    def get_file_type(self) -> str:
        """
        Trả về loại file dựa vào đuôi của file
        :return: Loại file
        """

        return os.path.split(self.file_path)[1].split(".")[1]

    def get_info(self) -> str:
        meta_data = self.__meta_data__ if self.__meta_data__ else self.data
        attr_names = [z for z in dir(meta_data) if not z.startswith("_")]
        info = {}
        for attr_name in attr_names:
            value = getattr(meta_data, attr_name)
            if (
                value is not None
                and value.__class__.__name__ in ["int", "str", "datetime"]
                and len(str(value)) > 0
            ):
                if value.__class__.__name__ in ["int", "str"]:
                    info[attr_name] = value
                else:
                    info[attr_name] = str(value)
        return info

    @abstractmethod
    def save(self, file_path=None, **args) -> bool:
        """
        Save file vào file_path
        :file_path: đường dẫn output file,
                    nếu file_path là None thì tự tạo tên file và save vào cache
        :return: trả về đường dẫn tới file
        """
