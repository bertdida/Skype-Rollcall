from sqlalchemy import Column, Integer, String
from skyperollcall.models import Base
from skyperollcall.models.mixins.BaseMixin import BaseMixin


class Channel(Base, BaseMixin):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    skype_id = Column(String(255), unique=True)
