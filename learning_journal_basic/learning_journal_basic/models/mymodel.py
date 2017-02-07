"""Setting up Models."""
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime
)

from .meta import Base


class MyEntry(Base):
    """Creating our Model Class."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    blog_entry = Column(Unicode)
    creation_date = Column(DateTime)
