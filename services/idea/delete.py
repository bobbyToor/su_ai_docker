import logging as logger

from sqlalchemy.orm import Session

from services.dbs.milvus_db import *
from services.dbs.sql_crud import *
from models import *

from common.config import MILVUS_COLLECTION


# deleting does not permanently deletes the idea
# it just marks deleted flag to True
# The children of this deleted idea can be
# used in a future remix of any similar parent idea
def delete_idea(db: Session, vdb: Milvus, fid: str):

    # get vector_ids
    ideas = get_ideas(db, fid)
    if not ideas:
        return None

    logger.info(f"Deleting idea, fid : {fid}")

    vector_ids = [e.vector_id for e in ideas]

    # mark deleted
    mark_delete_ideas_by_fid(db, fid)
    logger.info(f"Deleted vector_ids from db for fid : {fid}")

    # delete old vectors(if any) from vector db
    status = delete_vectors(vdb, MILVUS_COLLECTION, vector_ids)
    logger.info(f"Delete idea from milvus: fid {fid}, status : {status}")

    return status
