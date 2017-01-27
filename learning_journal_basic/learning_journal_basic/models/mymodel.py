from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    DateTime
)

from .meta import Base


class MyEntry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    blog_entry = Column(Unicode)
    creation_date = Column(DateTime)


# Index('my_index', MyEntry.title, unique=True, mysql_length=255)
