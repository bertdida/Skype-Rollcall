from skpy.msg import SkypeMsg
from skyperollcall.models import session, User, Channel, ChannelUser
from skyperollcall import utils


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
        users = [user for user in event.msg.chat.users]
        ignored_users = ChannelUser.get_ignored()

        user_names = []
        for curr_user in ignored_users:
            user = next((u for u in users if u.id == curr_user.skype_id), None)
            if user:
                user_names.append(f"{user.name.first} {user.name.last}")

        if not user_names:
            return

        message = "{title}\n{names}".format(
            title=SkypeMsg.bold("Ignored Users"),
            names="\n".join([f"- {n}" for n in user_names]),
        )

        event.msg.chat.sendMsg(message, rich=True)