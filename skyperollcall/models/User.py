from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from skyperollcall.models import Base
from skyperollcall.models.mixins import BaseMixin


class User(Base, BaseMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    skype_id = Column(String, unique=True, nullable=False)

    channels = relationship("Channel", secondary="channel_user", back_populates="users")
    groups = relationship("Group", secondary="group_user", back_populates="users")

    @classmethod
    def get_from_mentions(cls, channel, mentions):
        from skyperollcall.models import ChannelUser

        retval = []
        for mention in mentions:
            user = cls.first_or_create(skype_id=mention.id)
            ChannelUser.first_or_create(channel_id=channel.id, user_id=user.id)
            retval.append(user)

        return retval
