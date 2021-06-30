from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, BigInteger
from sqlalchemy.sql.sqltypes import Boolean, Integer, VARCHAR

Base = declarative_base()


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(VARCHAR(255), index=True, primary_key=True)
    fid = Column(VARCHAR(255))
    uid = Column(VARCHAR(255))
    vector_id = Column(BigInteger)
    title = Column(Text)
    description = Column(Text)
    emoji = Column(Text)
    is_public = Column(Boolean)
    deleted = Column(Boolean, default=False)
    path = Column(Text)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
