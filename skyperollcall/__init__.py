from skpy import SkypeEventLoop, SkypeGroupChat, SkypeNewMessageEvent

from config import config
from skyperollcall import utils
from skyperollcall.models import ChannelUser

commands = utils.load_commands()


class MySkypeEventLoop(SkypeEventLoop):
    def __init__(self, **kwargs):
        username = config.USERNAME
        password = config.PASSWORD

        super(MySkypeEventLoop, self).__init__(username, password, **kwargs)

    def onEvent(self, event):
        event.client = self

        if not isinstance(event, SkypeNewMessageEvent):
            return

        if not isinstance(event.msg.chat, SkypeGroupChat):
            return

        user = ChannelUser.from_event(event)
        if self.user.id != event.msg.user.id and not user.is_admin:
            return

        if not event.msg.plain:
            return

        if not event.msg.plain.startswith(config.COMMAND_PREFIX):
            return

        [command, *_] = event.msg.plain.lower().split()
        command = command[1:]
        Command = next((c for c in commands if c.name == command), None)

        if Command is not None:
            Command.execute(event)
