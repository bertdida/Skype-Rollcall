import threading


class RollCall:
    name = "rollcall"
    check_replies_interval = 60  # seconds

    @staticmethod
    def _create_mention(user):
        return f'<at id="{user.id}">{user.name.first}</at>'

    @staticmethod
    def _check_replies(event):
        message = event.msg
        author = message.user
        channel = message.chat

        responsive_users = []
        while True:
            for curr_message in channel.getMsgs():
                curr_author = curr_message.user
                if curr_message.id != message.id and curr_author.id != author.id:
                    responsive_users.append(curr_author.id)
                break
            else:
                continue
            break

        users = [user for user in channel.users]
        responsive_users = set(responsive_users)

        unresponsive_users = [user for user in users if user.id not in responsive_users]
        mentions = [RollCall._create_mention(user) for user in unresponsive_users]

        channel.sendMsg(" ".join(mentions), rich=True)

    @classmethod
    def execute(cls, event):
        interval = float(cls.check_replies_interval)
        threading.Timer(interval, cls._check_replies, [event]).start()