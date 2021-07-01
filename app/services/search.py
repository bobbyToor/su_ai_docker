from crud.crud_user import CRUDUser
import logging as logger
import random
from typing import List

from models.idea import Idea
from milvus import Milvus
from db.milvus_db import get_by_id, search_vectors
from crud.crud_idea import CRUDIdea

from core.config import L2_DISTANCE_THRESHOLD

# current strategy =
# return all similar child ideas in a random order
def get_children_ideas(
    crud_idea: CRUDIdea, crud_user: CRUDUser, vdb: Milvus, idea_id: str
):

    current_idea = crud_idea.fetch_by_id(idea_id)
    if not current_idea:
        logger.warning(f"Unknown id received : {idea_id}")
        return []

    current_children = crud_idea.get_1st_children([current_idea])

    similar_parents = get_similar_parent_ideas(crud_idea, vdb, idea_id)
    similar_parents_children = crud_idea.get_1st_children(similar_parents)

    # hacky ranking
    total_children = current_children + similar_parents_children
    total_children = list(set(total_children))
    random.shuffle(total_children)
    random_children = total_children[:7]

    uids = [cid.uid for cid in random_children]
    uids = list(set(uids))

    # get all corresponding users
    users = crud_user.fetch_by_ids(uids)
    users_dict = {user.id: user for user in users}

    if len(users_dict.keys()) != len(uids):
        logger.error("Users not updated")
        return []

    child_ideas_processed = []

    for child_idea in random_children:
        uid = child_idea.uid
        user = users_dict[uid]

        child_idea_processed = {
            "id": child_idea.id,
            "uid": uid,
            "title": child_idea.title,
            "description": child_idea.description,
            "emoji": child_idea.emoji,
            "children": [],
            "userPhotoUrl": user.photo_url,
            "userHandle": user.handle,
        }

        child_ideas_processed.append(child_idea_processed)

    return child_ideas_processed


def get_similar_parent_ideas(crud_idea: CRUDIdea, vdb: Milvus, idea_id: str):

    idea = crud_idea.fetch_by_id(idea_id)
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

    near_parent_ideas = crud_idea.fetch_by_vector_ids(sv_ids_near)
    return near_parent_ideas
