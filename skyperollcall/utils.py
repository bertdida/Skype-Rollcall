import importlib
import os
import re

from skpy import SkypeGroupChat, SkypeNewMessageEvent
from skpy.msg import SkypeMsg

from skyperollcall import commands
from skyperollcall.models import session


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


def validate_event(function):
    from functools import wraps

    @wraps(function)
    def wrapper(event, *args, **kwargs):
        if not isinstance(event, SkypeNewMessageEvent):
            raise ValueError

        if not isinstance(event.msg.chat, SkypeGroupChat):
            raise ValueError

        return function(event, *args, **kwargs)

    return wrapper


@validate_event
def get_mentions(event):
    args = get_args(event)
    users = [user for user in event.msg.chat.users]
    return [user for user in users if user.id in args]


@validate_event
def get_args(event):
    [_, *args] = re.split("\\s+", event.msg.plain.strip())
    return [arg.lstrip("@") for arg in args]


@validate_event
def send_name_list(event, users, title):
    if not users:
        return

    channel_users = [user for user in event.msg.chat.users]
    user_names = []

    for curr_user in users:
        user = next((u for u in channel_users if u.id == curr_user.skype_id), None)
        if user:
            user_names.append(f"{user.name.first} {user.name.last}")

    if not user_names:
        return

    message = "{title}\n{names}".format(
        title=SkypeMsg.bold(title),
        names="\n".join([f"- {n}" for n in user_names]),
    )

    event.msg.chat.sendMsg(message, rich=True)


def session_close():
    session.remove()
