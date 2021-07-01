import logging as logger
from crud.crud_idea import CRUDIdea

from db.milvus_db import Milvus, insert_vectors
from crud.crud_idea import CRUDIdea

from models.idea import Idea

from db.firestore_db import fetch_ideas
from services.embedder import get_idea_data_list

from services.idea.delete import delete_idea


def insert_idea(crud_idea: CRUDIdea, vdb: Milvus, idea_id: str):
    logger.info(f"Inserting idea : {idea_id}")

    # check if idea already exists
    # then delete it
    delete_idea(crud_idea, vdb, idea_id)

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
    status, vector_ids = insert_vectors(vdb, vectors)
    if len(vector_ids) != len(vectors):
        logger.error("Error insert vector, lengths not equal")

    logger.info(f"insert_vectors status : {status}")

    ideas_list = get_idea_models_from_ideas_list(idea_data_list, vector_ids)

    # inserts embedded ideas into mysql
    crud_idea.insert_embedded_ideas(ideas_list)


def get_idea_models_from_ideas_list(idea_data_list, vector_ids):
    ideas_list = []

    for index, idea_data in enumerate(idea_data_list):
        idea = Idea()

        idea.id = idea_data["id"]
        idea.fid = idea_data["fid"]
        idea.parent_id = idea_data["parent_id"]
        idea.vector_id = vector_ids[index]
        idea.uid = idea_data["uid"]
        idea.title = idea_data["title"]
        idea.description = idea_data["description"]
        idea.emoji = idea_data["emoji"]
        idea.is_public = idea_data["is_public"]
        idea.created_at = idea_data["created_at"]
        idea.updated_at = idea_data["updated_at"]

        ideas_list.append(idea)

    return ideas_list
