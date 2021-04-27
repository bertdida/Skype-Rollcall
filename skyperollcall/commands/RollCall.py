import threading
from skyperollcall.models import session, User, Channel, ChannelUser
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
        channel_db = Channel.get(skype_id=channel.id)

        unresponsive_users = []
        for user in users:
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

            channel_user.save()
            
            if channel_user.is_ignore == 1 or channel_user.is_admin == 1:
                pass

            elif user.id not in responsive_users and user.id != author.id:
                unresponsive_users.append(user)

        print(unresponsive_users)
        mentions = [utils.create_mention(user) for user in unresponsive_users]
        channel.sendMsg(" ".join(mentions), rich=True)

    @classmethod
    def execute(cls, event):
        interval = float(cls.check_replies_interval)
        threading.Timer(interval, cls._check_replies, [event]).start()