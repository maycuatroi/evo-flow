from evoflow.Entities.Common.Step.OpenExcelFile import OpenExcelFile


class ReadInputFile(OpenExcelFile):
    def __init__(self, **kwargs):
        self.file_path = None
        super().__init__(self.file_path, **kwargs)

    def prepare(self, config=None, **kwargs):
        self.file_path = config['data_source'] + config['InputFile']
