from evoflow.controller.data_manipulate.file_operator import FileOperator
from evoflow.entities.core.step import Step


class OpenExcelFile(Step):
    def __init__(self, file_path=None, **kwargs):
        """
        Open excel file
        Args:
            file_path: path to excel file
            **kwargs:
        """
        super().__init__(name="Open excel file", **kwargs)
        self.file_path = file_path
        self.kwars = kwargs

    def end(self, **kwargs) -> dict:
        return super().end(**kwargs)

    def prepare(self, **kwargs):
        super().prepare(**kwargs)

    def summary(self, **kwargs):
        return super().summary(**kwargs)

    def __info__(self, **kwargs) -> dict:
        return super().__info__(**kwargs)

    def action(self, **kwargs):
        reader = FileOperator()
        file = reader.read(file_path=self.file_path, **self.kwars)
        return {"file": file}
