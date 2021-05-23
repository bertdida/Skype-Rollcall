from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from skyperollcall.models import Base
from skyperollcall.models.mixins import BaseMixin


class Group(Base, BaseMixin):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)

    users = relationship("User", secondary="group_user", back_populates="groups")

    def add_users(self, users):
        from sqlalchemy.dialects.postgresql import insert

        from skyperollcall.models import session
        from skyperollcall.models.GroupUser import GroupUser

        values = [{"user_id": u.id, "group_id": self.id} for u in users]
        stmt = insert(GroupUser).values(values)
        stmt = stmt.on_conflict_do_nothing(index_elements=["user_id", "group_id"])
        session.execute(stmt)
        session.commit()

    def remove_users(self, users):
        from skyperollcall.models import session
        from skyperollcall.models.GroupUser import GroupUser

        composite_values = tuple(((self.id, u.id) for u in users))
        query = "DELETE FROM {table} WHERE (group_id, user_id) IN {composite_values}".format(  # noqa: E501
            table=GroupUser.__tablename__, composite_values=composite_values
        )

        session.execute(query)
        session.commit()
