from skyperollcall.models import session, User, Channel, ChannelUser
from skyperollcall import utils


class Admin:
    name = "admin"

    @classmethod
    def execute(cls, event):
        mentioned_users = utils.get_mentions(event)
        if not mentioned_users:
            return

        args = utils.get_args(event)
        make_admin = "--remove" not in args
        channel = Channel.get(skype_id=event.msg.chat.id)

        for curr_user in mentioned_users:
            user = User.first_or_create(skype_id=curr_user.id)
            channel_user = ChannelUser.first_or_create(
                user_id=user.id, channel_id=channel.id
            )

            channel_user.is_admin = make_admin
            if make_admin:
                channel_user.is_ignored = True

            channel_user.save()
