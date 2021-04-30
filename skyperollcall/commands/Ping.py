class Ping:
    name = "ping"

    @staticmethod
    def execute(event):
        event.msg.chat.sendMsg("pong")
