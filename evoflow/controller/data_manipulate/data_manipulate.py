from abc import abstractmethod


class DataManipulate:
    """
    Class object xử lý DATA
    """

    def authenticate(self, **args):
        """
        Thực hiện authenticate với data source
        :param args:
        :return:
        """

    @abstractmethod
    def read(self, file_path: str, **args):
        """
        Read file
        """
