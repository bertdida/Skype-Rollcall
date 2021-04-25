import threading
from skyperollcall import utils


class RollCall:
    name = "rollcall"
    check_replies_interval = 60  # seconds

    @staticmethod
    def _check_replies(event):
        message = event.msg
        author = message.user
        channel = message.chat

        responsive_users = []
        is_command_found = False

        while not is_command_found:
            for curr_message in channel.getMsgs():
                if curr_message.id == message.id:
                    is_command_found = True
                    break

                responsive_users.append(curr_message.user.id)

        users = [user for user in channel.users]
        responsive_users = set(responsive_users)

        unresponsive_users = []
        for user in users:
            if user.id not in responsive_users and user.id != author.id:
                unresponsive_users.append(user)

        mentions = [utils.create_mention(user) for user in unresponsive_users]
        channel.sendMsg(" ".join(mentions), rich=True)

    @classmethod
    def execute(cls, event):
        interval = float(cls.check_replies_interval)
        threading.Timer(interval, cls._check_replies, [event]).start()