from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from skyperollcall.models import Base
from skyperollcall.models.channeluser import ChannelUser
from skyperollcall.models.mixins.BaseMixin import BaseMixin


class User(Base, BaseMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    skype_id = Column(String, unique=True, nullable=False)

    channels = relationship("Channel", secondary="channel_user", back_populates="users")

    def is_admin(self, channel):
        channel_user = ChannelUser.get(user_id=self.id, channel_id=channel.id)
        return False if not channel_user else channel_user.is_admin