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
    def get_users_from_mentions(cls, mentions):
        from skyperollcall.models import session

        skype_ids = [u.id for u in mentions]
        return session.query(cls).filter(cls.skype_id.in_(skype_ids)).all()
