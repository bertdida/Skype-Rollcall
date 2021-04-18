import os
import sys
import importlib
import inspect
from skyperollcall import commands


def load_commands():
    path = os.path.dirname(os.path.abspath(commands.__file__))

    module_names = []
    for file_name in os.listdir(path):
        if file_name.endswith(".py") and file_name != "__init__.py":
            module_names.append(file_name[:-3])

    classes = []
    for module_name in module_names:
        module = importlib.import_module(".".join([commands.__name__, module_name]))

        for attribute in dir(module):
            if inspect.isclass(getattr(module, attribute)):
                classes.append(getattr(module, attribute))

    return classes