from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import config

Base = declarative_base()
engine = create_engine(config.DATABASE_URI, echo=True)

Session = sessionmaker(bind=engine)
session = scoped_session(Session)

# we have to import all models below for alembic
# autogenerate migration works
from skyperollcall.models.Channel import Channel  # noqa: E402, F401
from skyperollcall.models.ChannelUser import ChannelUser  # noqa: E402, F401
from skyperollcall.models.RollCall import RollCall  # noqa: E402, F401
from skyperollcall.models.RollCallLateResponder import (  # noqa: E402, F401
    RollCallLateResponder,
)
from skyperollcall.models.User import User  # noqa: E402, F401
