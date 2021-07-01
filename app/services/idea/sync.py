from crud.crud_user import CRUDUser
import logging as logger

from services.idea.insert import get_idea_models_from_ideas_list
from milvus import Milvus
from crud.crud_idea import CRUDIdea
from db.firestore_db import fetch_all_ideas, fetch_all_users
from db.milvus_db import drop_collection, init_table_milvus, insert_vectors
from services.embedder import get_idea_data_list
from db.utils import *
from models.user import User

# should do in batch
# currently can cause RAM issues
def sync(crud_idea: CRUDIdea, crud_user: CRUDUser, vdb: Milvus):
    logger.info(f"Syncing now ....")

    drop_collection(vdb)
    logger.info(f"Dropped milvus collection")

    drop_tables()
    logger.info(f"Dropped mysql tables")

    init_table_milvus(vdb)
    create_tables()

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
    status, vector_ids = insert_vectors(vdb, vectors)
    if len(vector_ids) != len(vectors):
        logger.error("Error insert vector, lengths not equal")
    logger.info(f"insert_vectors status, sync : {status}")

    idea_list = get_idea_models_from_ideas_list(ideas_data_list, vector_ids)

    ideas_data_list.clear()

    # inserts vector ids into mysql
    crud_idea.insert_embedded_ideas(idea_list)
    logger.info(f"total embeddings inserted : {len(idea_list)}")

    # now sync users
    users_dict = fetch_all_users()
    user_list = []

    for uid, user_dict in users_dict.items():
        user = User()

        user.id = uid
        user.handle = user_dict["handle"]
        user.first_name = user_dict["firstName"]
        user.last_name = user_dict["lastName"]
        user.photo_url = user_dict["photoUrl"]

        user_list.append(user)

    crud_user.bulk_save(user_list)
