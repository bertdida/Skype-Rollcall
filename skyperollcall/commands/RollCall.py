import threading

from skyperollcall import utils
from skyperollcall.models import Channel, ChannelUser, User


class RollCall:
    name = "rollcall"
    check_replies_interval = 60  # seconds

    @classmethod
    def execute(cls, event):
        interval = float(cls.check_replies_interval)
        threading.Timer(interval, cls._check_replies, [event]).start()

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
        channel_db = Channel.get(skype_id=channel.id)

        for user in users:
            user_db = User.first_or_create(skype_id=user.id)
            channel_user = ChannelUser.first_or_create(
                user_id=user_db.id, channel_id=channel_db.id
            )

            if channel_user.is_ignored or channel_user.is_admin:
                continue

            if user.id in responsive_users or user.id == author.id:
                continue

            unresponsive_users.append(user)

        if not unresponsive_users:
            return

        mentions = [utils.create_mention(user) for user in unresponsive_users]
        channel.sendMsg(" ".join(mentions), rich=True)
