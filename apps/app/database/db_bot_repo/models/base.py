from sqlalchemy.inspection import inspect
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BaseMixin:
    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
