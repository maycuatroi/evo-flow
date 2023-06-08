from evoflow.Controller.DataManipulate.FileOperator import FileOperator
from evoflow.Entities.Core.Step import Step


class OpenExcelFile(Step):

    def __init__(self, file_path='', **kwargs):
        """
        @param file_path:
        @param kwargs: pandas params
        """
        super().__init__(name='Open excel file', **kwargs)
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
        return {'file': file}


if __name__ == '__main__':
    step_open_excel = OpenExcelFile(file_path='data/Input.xlsx', header=12)
    results = step_open_excel.action()
    summary = results['file'].summary()
    print(summary)
