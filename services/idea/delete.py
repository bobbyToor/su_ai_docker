import logging as logger

from sqlalchemy.orm import Session

logger.basicConfig(level=logger.INFO)

from services.dbs.milvus_db import *
from services.dbs.sql_crud import *
from models import *

from common.config import MILVUS_COLLECTION


def delete_idea(db: Session, vdb: Milvus, idea_id: str):
    logger.info(f"Deleting idea : {idea_id}")

    # get vector_ids
    embeddings = get_embeddings_by_idea_id(db, idea_id)
    if not embeddings:
        return None

    vector_ids = [e.vector_id for e in embeddings]

    # delete old embeddings from mysql
    delete_embeddings_by_idea_id(db, idea_id)
    logger.info(f"Deleted vector_ids from mysql : {vector_ids}")

    # delete old vectors(if any) from vector db
    status = delete_vectors(vdb, MILVUS_COLLECTION, vector_ids)
    logger.info(f"Delete idea from milvus: {idea_id}, status : {status}")

    return status
