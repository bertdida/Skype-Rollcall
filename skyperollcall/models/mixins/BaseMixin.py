from sqlalchemy.exc import SQLAlchemyError

from skyperollcall.models import session


class BaseMixin:
    def __repr__(self):
        if not hasattr(self, "id"):
            return f"<{self.__class__.__name__}>"
        return f"<{self.__class__.__name__} id={self.id}>"

    @classmethod
    def get(cls, **kwargs):
        if not kwargs:
            return session.query(cls).first()

        return session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def get_all(cls, **kwargs):
        if not kwargs:
            return session.query(cls).all()

        return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def is_exists(cls, **kwargs):
        return session.query(session.query(cls).filter_by(**kwargs).exists()).scalar()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def first_or_create(cls, values={}, **kwargs):
        instance = cls.get(**kwargs)
        if instance:
            return instance

        return cls.create(**{**kwargs, **values})

    def update(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

        return self.save()

    def delete(self):
        session.delete(self)
        return session.commit()

    def save(self):
        session.add(self)

        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise

        return self
