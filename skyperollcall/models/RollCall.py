from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func

from skyperollcall.models import Base
from skyperollcall.models.mixins import BaseMixin


class RollCall(Base, BaseMixin):
    __tablename__ = "roll_call"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def add_users(self, users):
        from skyperollcall.models import engine
        from skyperollcall.models.RollCallLateResponder import RollCallLateResponder

        engine.execute(
            RollCallLateResponder.__table__.insert(),
            [{"user_id": u.id, "roll_call_id": self.id} for u in users],
        )
