from sqlalchemy import Column, Integer, Boolean, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.sql.expression import false
from skyperollcall import utils
from skyperollcall.models import Base
from skyperollcall.models.mixins.BaseMixin import BaseMixin


class ChannelUser(Base, BaseMixin):
    __tablename__ = "channel_user"
    __table_args__ = (PrimaryKeyConstraint("channel_id", "user_id"),)

    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_admin = Column(Boolean, server_default=false(), default=False)
    is_ignored = Column(Boolean, server_default=false(), default=False)

    @classmethod
    def from_event(cls, event):
        return utils.validate_event(cls._from_event)(event)

    @classmethod
    def _from_event(cls, event):
        from skyperollcall.models.User import User
        from skyperollcall.models.Channel import Channel

        channel = Channel.first_or_create(skype_id=event.msg.chat.id)
        user = User.first_or_create(skype_id=event.msg.user.id)
        return cls.first_or_create(channel_id=channel.id, user_id=user.id)