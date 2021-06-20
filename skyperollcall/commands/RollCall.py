import argparse
import shlex
from threading import Timer

from skyperollcall import utils
from skyperollcall.models import Channel, ChannelUser
from skyperollcall.models import Group as GroupModel
from skyperollcall.models import RollCall as RollCallModel
from skyperollcall.models import User


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


timer = None


class RollCall:
    name = "rollcall"

    @classmethod
    def execute(cls, event):
        global timer

        if timer and timer.is_alive():
            event.msg.chat.sendMsg("Rollcall is ongoing...")
            return

        parser = ThrowingArgumentParser()
        parser.add_argument("--until", default=5, type=float)
        parser.add_argument("--gimme", default="", type=str)
        parser.add_argument("--group", default="", type=str)

        user = User.get(skype_id=event.msg.user.id)
        roll_call = RollCallModel.create(user_id=user.id)

        try:
            args, *_ = parser.parse_known_args(shlex.split(event.msg.plain.strip()))

            group = None
            if args.group:
                group = GroupModel.get(name=args.group)
                if not group:
                    event.msg.chat.sendMsg(f"Error: Group {args.group} not found")
                    return

            timer_func_args = [event, args, roll_call, group]
            timer = Timer(args.until * 60, cls._check_replies, timer_func_args)
            timer.start()
        except ArgumentParserError as error:
            event.msg.chat.sendMsg(f"Error: {str(error)}")

    @staticmethod
    def _check_replies(event, args, roll_call, group=None):
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

                if not args.gimme or curr_message.content.strip() == args.gimme:
                    responsive_users.append(curr_message.user.id)

        users = [user for user in channel.users]
        if group:
            user_ids = [user.skype_id for user in group.users]
            users = [user for user in users if user.id in user_ids]

        responsive_users = set(responsive_users)

        unresponsive_users = []
        roll_call_users = []
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

            if user.id == event.client.user.id:
                continue

            unresponsive_users.append(user)
            roll_call_users.append(user_db)

        if not unresponsive_users:
            return

        roll_call.add_users(roll_call_users)

        unresponsive_users.sort(key=RollCall._sort_users_key)
        mentions = [utils.create_mention(user) for user in unresponsive_users]
        channel.sendMsg(" ".join(mentions), rich=True)

    @staticmethod
    def _sort_users_key(user):
        return utils.get_mention_name(user).lower()
