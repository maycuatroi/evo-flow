import os

from evoflow.Controller.DataManipulate.FileOperator import FileOperator
from evoflow.Entities.Core.Step import Step
from evoflow.Entities.Global import Global


class OpenCATIAFile(Step):
    def __init__(
            self, name: str = None, transactions=None, file_name: str = '', **kwargs
    ):
        '''

        @param file_name: Đường dẫn tới CATIA File
        '''
        super().__init__(name, transactions, **kwargs)
        self.file_name = file_name

    def action(self, **kwargs):
        if not self.params.get('FILE_NAME'):
            print('[OPENING CATIA]')
            self.file_name = os.getenv('CATIA_FILE_NAME') or input('Enter CATIA file name: ')
            if self.file_name is None:
                caa = Global().caa
                return {'catia_file': caa.active_document}
            self.file_name = self.file_name.strip('"')
        file = FileOperator().read(self.file_name)

        return {'catia_file': file}
