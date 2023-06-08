import glob
import inspect
import os

import evoflow


def get_all_common_steps():
    current_dir = os.path.split(__file__)[0]
    cwd = os.path.split(os.getcwd())[0]
    file_paths = glob.glob(f"{current_dir}/*.py")
    data = {}
    for file_path in file_paths:
        file_path = os.path.normpath(file_path)
        file_path = file_path.replace(cwd, "")
        if file_path.startswith("__init__"):
            continue

        import_string = file_path.replace(os.sep, ".")[:-3][1:]
        imported_module = __import__(
            import_string, fromlist=import_string.split(".")[-1]
        )

        for class_name, import_class in inspect.getmembers(imported_module):
            if class_name == import_string.split(".")[-1]:
                data[class_name] = import_class()
                break
    return data


@evoflow.Step()
def show_menu(menu_dict: dict = {}):
    for key, value in menu_dict.items():
        print(f"{key}. {value}")
    select_option = os.environ.get("SELECT_OPTION") or input("Enter your option: ")
    return {"select_option": int(select_option)}
