from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint

from skyperollcall.models import Base
from skyperollcall.models.mixins import BaseMixin


class GroupUser(Base, BaseMixin):
    __tablename__ = "group_user"
    __table_args__ = (PrimaryKeyConstraint("group_id", "user_id"),)

    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
