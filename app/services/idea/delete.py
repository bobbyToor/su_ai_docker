import logging as logger

from db.milvus_db import delete_vectors

from crud.crud_idea import CRUDIdea
from milvus import Milvus
from core.config import MILVUS_COLLECTION


# deleting does not permanently deletes the idea
# it just marks deleted flag to True
# The children of this deleted idea can be
# used in a future remix of any similar parent idea
def delete_idea(crud_idea: CRUDIdea, vdb: Milvus, fid: str):

    # get vector_ids
    ideas = crud_idea.fetch_by_fid(fid)
    if not ideas:
        return None

    logger.info(f"Deleting idea, fid : {fid}")

    vector_ids = [e.vector_id for e in ideas]

    # mark deleted
    crud_idea.mark_delete_ideas_by_fid(fid)
    logger.info(f"Deleted vector_ids from db for fid : {fid}")

    # delete old vectors(if any) from vector db
    status = delete_vectors(vdb, MILVUS_COLLECTION, vector_ids)
    logger.info(f"Delete idea from milvus: fid {fid}, status : {status}")

    return status
