from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# we have to import all models below for alembic
# autogenerate migration works
from skyperollcall.models.channel import Channel