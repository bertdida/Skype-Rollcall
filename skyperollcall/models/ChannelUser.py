from sqlalchemy import Boolean, Column, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.sql.expression import false

from skyperollcall import utils
from skyperollcall.models import Base, session
from skyperollcall.models.mixins import BaseMixin


class ChannelUser(Base, BaseMixin):
    __tablename__ = "channel_user"
    __table_args__ = (PrimaryKeyConstraint("channel_id", "user_id"),)

    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_admin = Column(Boolean, server_default=false(), default=False)
    is_ignored = Column(Boolean, server_default=false(), default=False)

    def __repr__(self):
        return f"<ChannelUser user_id={self.user_id} channel_id={self.channel_id}>"

    @classmethod
    def from_event(cls, event):
        return utils.validate_event(cls._from_event)(event)

    @classmethod
    def _from_event(cls, event):
        from skyperollcall.models.Channel import Channel
        from skyperollcall.models.User import User

        channel = Channel.first_or_create(skype_id=event.msg.chat.id)
        user = User.first_or_create(skype_id=event.msg.user.id)
        return cls.first_or_create(channel_id=channel.id, user_id=user.id)

    @classmethod
    def get_ignored(cls):
        from skyperollcall.models.User import User

        return session.query(User).join(cls).filter(cls.is_ignored).all()

    @classmethod
    def get_admins(cls):
        from skyperollcall.models.User import User

        return session.query(User).join(cls).filter(cls.is_admin).all()
