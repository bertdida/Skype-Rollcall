from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from skyperollcall.models import Base
from skyperollcall.models.mixins.BaseMixin import BaseMixin


class User(Base, BaseMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    skype_id = Column(String, unique=True, nullable=False)

    channels = relationship("Channel", secondary="channel_user", back_populates="users")
