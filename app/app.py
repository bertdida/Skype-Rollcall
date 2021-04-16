import os
from skpy import SkypeEventLoop, SkypeNewMessageEvent, SkypeGroupChat


username = os.environ["SKYPE_USERNAME"]
password = os.environ["SKYPE_PASSWORD"]


class MySkypeEventLoop(SkypeEventLoop):
    def onEvent(self, event):
        if not isinstance(event, SkypeNewMessageEvent):
            return

        if not isinstance(event.msg.chat, SkypeGroupChat):
            return

        if event.msg.userId == self.userId:
            return

        print(repr(event))


if __name__ == "__main__":
    sk = MySkypeEventLoop(username, password, autoAck=True)
    sk.loop()
