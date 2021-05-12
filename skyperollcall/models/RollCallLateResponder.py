from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint

from skyperollcall.models import Base
from skyperollcall.models.mixins import BaseMixin


class RollCallLateResponder(Base, BaseMixin):
    __tablename__ = "roll_call_late_responder"
    __table_args__ = (PrimaryKeyConstraint("roll_call_id", "user_id"),)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    roll_call_id = Column(Integer, ForeignKey("roll_call.id"), nullable=False)

    def __repr__(self):
        return f"<RollCallLateResponder user_id={self.user_id} roll_call_id={self.roll_call}>"  # noqa: E501
