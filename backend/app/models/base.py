"""Declarative base for all ORM models.

Living in its own module so models can import Base without pulling in
sibling models (which would create import cycles for relationships).
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
