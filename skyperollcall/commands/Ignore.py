from skyperollcall import utils
from skyperollcall.models import Channel, ChannelUser, User


class Ignore:
    name = "ignore"

    @classmethod
    def execute(cls, event):
        mentioned_users = utils.get_mentions(event)
        if not mentioned_users:
            cls.send_ignored_users(event)
            return

        args = utils.get_args(event)
        channel = Channel.get(skype_id=event.msg.chat.id)

        for curr_user in mentioned_users:
            user = User.first_or_create(skype_id=curr_user.id)
            channel_user = ChannelUser.first_or_create(
                user_id=user.id, channel_id=channel.id
            )

            channel_user.is_ignored = "--remove" not in args
            channel_user.save()

        cls.send_ignored_users(event)

    @classmethod
    def send_ignored_users(cls, event):
        users = ChannelUser.get_ignored()
        if not users:
            return

        utils.send_name_list(event, users=users, title="Ignored Users")
