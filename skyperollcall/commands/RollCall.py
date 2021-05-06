import argparse
import shlex
import threading

from skyperollcall import utils
from skyperollcall.models import Channel, ChannelUser, User


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


class RollCall:
    name = "rollcall"

    @classmethod
    def execute(cls, event):
        parser = ThrowingArgumentParser()
        parser.add_argument("--until", default=5, type=float)
        parser.add_argument("--gimme", default="", type=str)

        try:
            args, *_ = parser.parse_known_args(shlex.split(event.msg.plain.strip()))
            threading.Timer(args.until * 60, cls._check_replies, [event, args]).start()
        except ArgumentParserError as error:
            event.msg.chat.sendMsg(f"Error: {str(error)}")

    @staticmethod
    def _check_replies(event, args):
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

                if not args.gimme or curr_message.content == args.gimme:
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
        utils.session_close()
