from db_manager import DbManager
import logging as logger

from sqlalchemy.orm import Session

from services.dbs.milvus_db import *
from services.dbs.sql_crud import *
from services.idea.insert import get_idea_models_from_ideas_list
from models import *

from services.dbs.firestore_db import fetch_all_ideas
from services.embedder import get_idea_data_list
from common.config import MILVUS_COLLECTION

# should do in batch
# currently can cause RAM issues
def sync(dbm: DbManager):
    logger.info(f"Syncing now ....")

    db = dbm.get_db()
    vdb = dbm.get_vdb()

    drop_collection(vdb)
    logger.info(f"Dropped milvus collection")

    dbm.delete_db_tables()
    logger.info(f"Dropped mysql tables")

    init_table_milvus(vdb)
    dbm.create_db_tables()

    vectors = []
    ideas_data_list = []

    docs_dict = fetch_all_ideas()

    for idea_id, doc_data in docs_dict.items():

        idea_data_list = get_idea_data_list(idea_id, doc_data)
        ideas_data_list += idea_data_list

        doc_vectors = [v["title_vector"].tolist() for v in idea_data_list]
        vectors += doc_vectors

    docs_dict.clear()

    # create vector ids
    status, vector_ids = insert_vectors(vdb, MILVUS_COLLECTION, vectors)
    if len(vector_ids) != len(vectors):
        logger.error("Error insert vector, lengths not equal")
    logger.info(f"insert_vectors status, sync : {status}")

    idea_list = get_idea_models_from_ideas_list(ideas_data_list, vector_ids)

    ideas_data_list.clear()

    # inserts vector ids into mysql
    insert_embedded_ideas(db, idea_list)
    logger.info(f"total embeddings inserted : {len(idea_list)}")
