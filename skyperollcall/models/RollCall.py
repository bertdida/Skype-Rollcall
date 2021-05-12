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
