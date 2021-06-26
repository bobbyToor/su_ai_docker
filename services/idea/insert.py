import logging as logger

from sqlalchemy.orm import Session

logger.basicConfig(level=logger.INFO)

from services.dbs.milvus_db import *
from services.dbs.sql_crud import *
from models import *

from services.dbs.firestore_db import fetch_ideas, fetch_all_ideas
from services.embedder import get_title_embeddings
from common.config import MILVUS_COLLECTION

from services.idea.delete import delete_idea


def insert_idea(db: Session, vdb: Milvus, idea_id: str):
    logger.info(f"Inserting idea : {idea_id}")

    # check if idea already exists
    # then delete it
    delete_idea(db, vdb, idea_id)

    # now insert new one
    # generate embeddings based on titles only (for now)
    ideas_dict = fetch_ideas([idea_id])
    doc_data = ideas_dict[idea_id]

    if not doc_data:
        logger.error(f"idea not found in firestore : {idea_id}")
        return

    title_embeddings = get_title_embeddings(idea_id, doc_data)

    vectors = [v.tolist() for v in list(title_embeddings.values())]
    embedding_ids = list(title_embeddings.keys())

    # create vector ids
    status, vector_ids = insert_vectors(vdb, MILVUS_COLLECTION, vectors)
    logger.info(f"insert_vectors status : {status}")

    embeddings = []
    for i, vid in enumerate(vector_ids):
        eid = embedding_ids[i]

        embedding = Embedding()
        embedding.vector_id = vid
        embedding.embedding_id = eid
        embedding.idea_id = idea_id

        embeddings.append(embedding)

    # inserts vector ids into mysql
    insert_embeddings(db, embeddings)
