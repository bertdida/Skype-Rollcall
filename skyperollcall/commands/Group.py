import argparse
import shlex

from skpy.msg import SkypeMsg

from skyperollcall import utils
from skyperollcall.models import Channel
from skyperollcall.models import Group as GroupModel
from skyperollcall.models.User import User


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


class Group:
    name = "group"

    @classmethod
    def execute(cls, event):
        parser = ThrowingArgumentParser()
        parser.add_argument("--name", default="", type=str)

        try:
            args, *_ = parser.parse_known_args(shlex.split(event.msg.plain.strip()))
            mentions = utils.get_mentions(event)
            channel = Channel.get(skype_id=event.msg.chat.id)

            if not args.name:
                cls.send_group_names(event, channel)
                return

            group = GroupModel.get(name=args.name)

            if group:
                if "--delete" in utils.get_args(event):
                    group.delete()
                    cls.send_group_names(event, channel)
                    return

                if mentions:
                    users = User.get_users_from_mentions(mentions)

                    if "--remove" in utils.get_args(event):
                        group.remove_users(users)
                    else:
                        group.add_users(users)

                cls.send_group_users(event, group)
                return

            if not mentions:
                GroupModel.create(name=args.name, channel_id=channel.id)
                cls.send_group_names(event, channel)
                return

            event.msg.chat.sendMsg(f"Error: {args.name} not found")
        except ArgumentParserError as error:
            event.msg.chat.sendMsg(f"Error: {str(error)}")

    @staticmethod
    def send_group_names(event, channel):
        groups = GroupModel.get_all(channel_id=channel.id)

        if not groups:
            return

        message = "{title}\n{names}".format(
            title=SkypeMsg.bold("Groups"),
            names="\n".join([f"- {g.name}" for g in groups]),
        )

        event.msg.chat.sendMsg(message, rich=True)

    @staticmethod
    def send_group_users(event, group):
        users = group.users
        utils.send_name_list(event, users, f"{group.name} Users")
