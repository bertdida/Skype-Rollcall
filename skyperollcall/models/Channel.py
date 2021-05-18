from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from skyperollcall.models import Base, session
from skyperollcall.models.mixins import BaseMixin


class Channel(Base, BaseMixin):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    skype_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)

    users = relationship("User", secondary="channel_user", back_populates="channels")

    def get_ignored(self):
        from skyperollcall.models.ChannelUser import ChannelUser
        from skyperollcall.models.User import User

        return (
            session.query(User)
            .join(ChannelUser)
            .join(self.__class__)
            .filter(ChannelUser.is_ignored, ChannelUser.channel_id == self.id)
            .all()
        )

    def get_admins(self):
        from skyperollcall.models.ChannelUser import ChannelUser
        from skyperollcall.models.User import User

        return (
            session.query(User)
            .join(ChannelUser)
            .join(self.__class__)
            .filter(ChannelUser.is_admin, ChannelUser.channel_id == self.id)
            .all()
        )
