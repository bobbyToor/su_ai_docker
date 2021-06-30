import logging as logger

from sqlalchemy.orm import Session

from services.dbs.milvus_db import Milvus, insert_vectors
from services.dbs.sql_crud import insert_embedded_ideas
from models import Idea

from services.dbs.firestore_db import fetch_ideas
from services.embedder import get_idea_data_list
from common.config import MILVUS_COLLECTION

from services.idea.delete import delete_idea


def insert_idea(db: Session, vdb: Milvus, idea_id: str):
    logger.info(f"Inserting idea : {idea_id}")

    # check if idea already exists
    # then delete it
    delete_idea(db, vdb, idea_id)

    # now insert new one
    # generate embeddings based on titles only (for now)
    idea_dict = fetch_ideas([idea_id])
    doc_data = idea_dict[idea_id]

    if not doc_data:
        logger.error(f"idea not found in firestore : {idea_id}")
        return

    idea_data_list = get_idea_data_list(idea_id, doc_data)

    vectors = [v["title_vector"].tolist() for v in idea_data_list]

    # create vector ids
    status, vector_ids = insert_vectors(vdb, MILVUS_COLLECTION, vectors)
    if len(vector_ids) != len(vectors):
        logger.error("Error insert vector, lengths not equal")

    logger.info(f"insert_vectors status : {status}")

    ideas_list = get_idea_models_from_ideas_list(idea_data_list, vector_ids)

    # inserts embedded ideas into mysql
    insert_embedded_ideas(db, ideas_list)


def get_idea_models_from_ideas_list(idea_data_list, vector_ids):
    ideas_list = []

    for index, idea_data in enumerate(idea_data_list):
        idea = Idea()

        idea.id = idea_data["id"]
        idea.fid = idea_data["fid"]
        idea.vector_id = vector_ids[index]
        idea.uid = idea_data["uid"]
        idea.title = idea_data["title"]
        idea.description = idea_data["description"]
        idea.emoji = idea_data["emoji"]
        idea.is_public = idea_data["is_public"]
        idea.path = idea_data["path"]
        idea.created_at = idea_data["created_at"]
        idea.updated_at = idea_data["updated_at"]

        ideas_list.append(idea)

    return ideas_list
