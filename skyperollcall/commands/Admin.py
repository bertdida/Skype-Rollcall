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
            user_db = User.get(skype_id=user.id)

            if not user_db:
                user_db = User()
                user_db.skype_id = user.id

            user_db = user_db.save()
            channel_user = ChannelUser.get(user_id=user_db.id, channel_id=channel_db.id)

            if not channel_user:
                channel_user = ChannelUser()
                channel_user.user_id = user_db.id
                channel_user.channel_id = channel_db.id

            channel_user.is_admin = "--remove" not in args
            channel_user.save()
