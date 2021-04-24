from sqlalchemy import Column, Integer, String, Boolean
from skyperollcall.models import Base


class User(Base):
     __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    skype_id = Column(String(255), unique=True)
    ignore_user = Column(Boolean)
    admin = Column(Boolean)
    channel_id = relationship("Channel",backref="user",order_by="Chennel.id")