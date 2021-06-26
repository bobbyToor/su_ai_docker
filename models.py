from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, BigInteger

Base = declarative_base()


class Embedding(Base):
    __tablename__ = "embeddings"

    vector_id = Column(BigInteger, index=True, primary_key=True)
    embedding_id = Column(Text)
    idea_id = Column(Text)
