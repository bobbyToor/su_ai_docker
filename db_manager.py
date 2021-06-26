import logging as logger
from common.config import (
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_DB,
)

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

import models

from services.dbs.milvus_db import get_milvus_client, init_table_milvus, total_count


SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_embeddings_table():
    models.Base.metadata.create_all(bind=engine, tables=[models.Embedding.__table__])


def delete_embeddings_table():
    models.Base.metadata.drop_all(bind=engine, tables=[models.Embedding.__table__])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_vdb():
    return get_milvus_client()


create_embeddings_table()

milvus_client = get_vdb()
init_table_milvus(milvus_client)

logger.info(f"Total vector count : {total_count(milvus_client)}")
