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

        channelDb = Channel.get(skype_id=channel.id)

        for user in mentioned_users:
            userDb = User.get(skype_id=user.id)
            if not userDb:
                userDb = User()
                userDb.skype_id = user.id

            userDb = userDb.save()
            channelUserDb = ChannelUser.get(user_id=userDb.id, channel_id=channelDb.id)

            if not channelUserDb:
                channelUserDb = ChannelUser()
                channelUserDb.user_id = userDb.id
                channelUserDb.channel_id = channelDb.id

            channelUserDb.is_admin = True
            channelUserDb.save()
