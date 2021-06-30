import logging as logger
import random

from sqlalchemy.orm import Session
from milvus import Milvus

from services.dbs.firestore_db import fetch_ideas, fetch_users

from services.dbs.sql_crud import *
from services.dbs.milvus_db import get_by_id, search_vectors

from common.config import L2_DISTANCE_THRESHOLD

# current strategy =
# return all similar child ideas in a random order
def get_children_ideas(db: Session, vdb: Milvus, idea_id: str):

    current_idea = fetch_by_id(db, idea_id)
    if not current_idea:
        logger.warning(f"Unknown id received : {idea_id}")
        return []

    current_children = get_1st_children(db, [current_idea])

    similar_parents = get_similar_parent_ideas(db, vdb, idea_id)
    similar_parents_children = get_1st_children(db, similar_parents)

    # hacky ranking
    total_children = current_children + similar_parents_children
    total_children = list(set(total_children))
    random.shuffle(total_children)
    random_children = total_children[:7]

    uids = [cid.uid for cid in random_children]

    # create user table in mysql too
    # dont fetch from firestore
    users_dict = fetch_users(uids)

    child_ideas_processed = []

    for child_idea in random_children:
        uid = child_idea.uid
        user = users_dict[uid]

        child_idea_processed = {
            "id": child_idea.id,
            "uid": uid,
            "path": child_idea.path,
            "title": child_idea.title,
            "description": child_idea.description,
            "emoji": child_idea.emoji,
            "children": [],
            "userPhotoUrl": user["photoUrl"],
            "userHandle": user["handle"],
        }

        child_ideas_processed.append(child_idea_processed)

    return child_ideas_processed


def get_similar_parent_ideas(db: Session, vdb: Milvus, idea_id: str):

    idea = fetch_by_id(db, idea_id)
    if not idea:
        return []

    vector_id = idea.vector_id

    result_vectors = get_by_id(vdb, vector_id)  # length is always 1

    search_vectors_res_dict = search_vectors(vdb, result_vectors)

    # get ideas whose distance is less than threshold
    sv_ids = list(search_vectors_res_dict.keys())
    sv_ids_near = [
        svid
        for svid in sv_ids
        if search_vectors_res_dict[svid] <= L2_DISTANCE_THRESHOLD
    ]

    near_parent_ideas = fetch_by_vector_ids(db, sv_ids_near)
    return near_parent_ideas


def get_1st_children(db: Session, parents: List[Idea]):
    if not parents:
        return []

    path_queries = []

    for idea in parents:
        path = idea.path
        path_queries.append(f"{path},[^,]*$")

    children = search_by_paths(db, path_queries)
    return children
