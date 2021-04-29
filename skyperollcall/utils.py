import os
import re
import sys
import importlib
import inspect
from skpy import SkypeNewMessageEvent, SkypeGroupChat
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


def get_mentions(event):
    if not isinstance(event, SkypeNewMessageEvent):
        raise ValueError

    if not isinstance(event.msg.chat, SkypeGroupChat):
        raise ValueError

    args = get_args(event)
    users = [user for user in event.msg.chat.users]
    return [user for user in users if user.id in args]


def get_args(event):
    if not isinstance(event, SkypeNewMessageEvent):
        raise ValueError

    if not isinstance(event.msg.chat, SkypeGroupChat):
        raise ValueError

    [_, *args] = re.split("\s+", event.msg.plain.strip())
    return [arg.lstrip("@") for arg in args]