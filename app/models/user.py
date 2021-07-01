from sqlalchemy import Column, Text, BigInteger
from sqlalchemy.sql.sqltypes import Boolean, VARCHAR

from db.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(VARCHAR(255), index=True, primary_key=True)
    handle = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    photo_url = Column(Text)
