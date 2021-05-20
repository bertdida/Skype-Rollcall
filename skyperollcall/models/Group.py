from sqlalchemy import Column, ForeignKey, Integer, String

from skyperollcall.models import Base
from skyperollcall.models.mixins import BaseMixin


class Group(Base, BaseMixin):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
