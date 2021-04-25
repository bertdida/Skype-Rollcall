import os
from skpy import SkypeEventLoop, SkypeNewMessageEvent, SkypeGroupChat
from skyperollcall import utils
from skyperollcall.models import Channel

commands = utils.load_commands()


class MySkypeEventLoop(SkypeEventLoop):
    def __init__(self, config, **kwargs):
        self.config = config
        username = config.USERNAME
        password = config.PASSWORD

        super(MySkypeEventLoop, self).__init__(username, password, **kwargs)

    def onEvent(self, event):
        if not isinstance(event, SkypeNewMessageEvent):
            return

        if not isinstance(event.msg.chat, SkypeGroupChat):
            return

        if not Channel.is_exists(skype_id=event.msg.chat.id):
            Channel.create(skype_id=event.msg.chat.id)

        if not event.msg.plain.startswith(self.config.COMMAND_PREFIX):
            return

        if self.config.GROUP_IDS and event.msg.chat.id not in self.config.GROUP_IDS:
            return

        [command, *args] = event.msg.plain.lower().split()
        command = command[1:]
        Command = next((c for c in commands if c.name == command), None)

        if Command is not None:
            Command.execute(event)