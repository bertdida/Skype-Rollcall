from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from skyperollcall.models import Base
from skyperollcall.models.mixins import BaseMixin


class Channel(Base, BaseMixin):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    skype_id = Column(String, unique=True, nullable=False)

    users = relationship("User", secondary="channel_user", back_populates="channels")
