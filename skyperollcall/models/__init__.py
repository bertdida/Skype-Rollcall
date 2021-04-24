from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config

Base = declarative_base()
engine = create_engine(config.DATABASE_URI, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

# we have to import all models below for alembic
# autogenerate migration works
from skyperollcall.models.channel import Channel