from evoflow.Entities.Core.Step import Step
from evoflow.Entities.Global import Global


class GetObjectsByName(Step):
    def action(self):
        caa = Global().caa
        caa.active_document.selection.search(f'Name={self.object_name},all')
        return {'objects': caa.active_document.selection.items()}
