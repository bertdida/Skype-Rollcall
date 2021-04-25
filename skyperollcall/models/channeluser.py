from sqlalchemy import Column, Integer, PrimaryKeyConstraint, ForeignKey
from skyperollcall.models import Base
from skyperollcall.models.mixins.BaseMixin import BaseMixin


class ChannelUser(Base, BaseMixin):
    __tablename__ = "channel_user"
    __table_args__ = (PrimaryKeyConstraint("channel_id", "user_id"),)

    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
