import abc

import json_tricks as json


class AbstractData:
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_info(self) -> str:
        """
        print một đoạn mô tả về data object này
        :return:
        """
        info = {"info": "Abstract data"}
        return info

    def summary(self):
        """
        Summary info of current object
        """
        info = self.get_info()
        return json.dumps(info, ensure_ascii=False, indent=2)

    @abc.abstractmethod
    def save(self, file_path, **args) -> str:
        """
        Lưu data này lại
        :param args:
        :return: đường dẫn tới file sau khi save ra
        """

        raise NotImplementedError()
