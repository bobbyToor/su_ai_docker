import logging as logger
from db.config import Base, engine
from api.dependencies import get_vdb
from db.milvus_db import init_table_milvus, total_count


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(bind=engine)


def init_db():
    create_tables()
    milvus_client = get_vdb()
    init_table_milvus(milvus_client)
    total_v_count = total_count(milvus_client)
    logger.info(f"Total vector count : {total_v_count}")
