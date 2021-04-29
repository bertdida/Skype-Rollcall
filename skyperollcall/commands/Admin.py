import re
from skyperollcall.models import session, User, Channel, ChannelUser
from skyperollcall import utils


class Admin:
    name = "admin"

    @classmethod
    def execute(cls, event):
        message = event.msg.plain.strip()
        channel = event.msg.chat

        [_, *args] = re.split("\s+", message)
        args = [arg.lstrip("@") for arg in args]

        users = [user for user in channel.users]
        mentioned_users = [user for user in users if user.id in args]

        if not mentioned_users:
            return

        channel_db = Channel.get(skype_id=channel.id)

        for user in mentioned_users:
            user_db = User.first_or_create(skype_id=user.id)
            channel_user = ChannelUser.first_or_create(
                user_id=user_db.id, channel_id=channel_db.id
            )

            channel_user.is_admin = "--remove" not in args
            channel_user.save()
