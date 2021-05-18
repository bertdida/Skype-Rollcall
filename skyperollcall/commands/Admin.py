from skyperollcall import utils
from skyperollcall.models import Channel, ChannelUser, User


class Admin:
    name = "admin"

    @classmethod
    def execute(cls, event):
        mentioned_users = utils.get_mentions(event)
        channel = Channel.get(skype_id=event.msg.chat.id)

        if not mentioned_users:
            cls.send_admin_users(event, channel)
            return

        args = utils.get_args(event)
        make_admin = "--remove" not in args

        for curr_user in mentioned_users:
            user = User.first_or_create(skype_id=curr_user.id)
            channel_user = ChannelUser.first_or_create(
                user_id=user.id, channel_id=channel.id
            )

            if user.skype_id == event.client.user.id:
                continue

            channel_user.is_admin = make_admin
            if make_admin:
                channel_user.is_ignored = True

            channel_user.save()

        cls.send_admin_users(event, channel)

    @classmethod
    def send_admin_users(cls, event, channel):
        users = channel.get_admins()
        if not users:
            return

        utils.send_name_list(event, users=users, title="Admin Users")
