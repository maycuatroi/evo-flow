from time import sleep

from evoflow.Entities.Global import Global


def add_text_with_leader(i_object=None, text=''):
    caa = Global().caa
    selection = caa.active_document.selection
    if i_object is not None:
        selection.clear()
        selection.add(i_object)
    caa.start_command('Text with leader')
    text_editor_window = caa.gui.window(title='Text Editor')
    text_editor_window.Edit.set_edit_text(text)
    text_editor_window.OK.click()


def disassemble(i_object=None):
    caa = Global().caa
    selection = caa.active_document.selection
    if i_object is not None:
        selection.clear()
        selection.add(i_object)
    caa.start_command('disassemble')
    text_editor_window = Global().caa.gui.window(title='Disassemble')
    text_editor_window.OK.click()
    sleep(2)
