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
        classes.append(getattr(module, module_name))

    return classes


def create_mention(user):
    return f'<at id="{user.id}">{user.name.first}</at>'