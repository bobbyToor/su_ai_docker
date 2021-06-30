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


class DbManager:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        self.sessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.neo = None

        self.create_db_tables()

        milvus_client = self.get_vdb()
        init_table_milvus(milvus_client)
        total_v_count = total_count(milvus_client)
        logger.info(f"Total vector count : {total_v_count}")

    def create_db_tables(self):
        models.Base.metadata.create_all(bind=self.engine)

    def delete_db_tables(self):
        models.Base.metadata.drop_all(bind=self.engine)

    def get_db(self):
        db = self.sessionLocal()
        return db
        # try:
        #     yield db
        # finally:
        #     db.close()

    def get_vdb(self):
        return get_milvus_client()

    def gdb_close(self):
        self.neo.close()
