import logging as logger

from sqlalchemy.orm import Session
from milvus import Milvus

from services.dbs.firestore_db import fetch_ideas, fetch_users

from services.dbs.sql_crud import *
from services.dbs.milvus_db import get_by_id, search_vectors

from common.config import L2_DISTANCE_THRESHOLD

# current strategy =
# return all similar child ideas in a random order
def get_children_ideas(db: Session, vdb: Milvus, embedding_id: str):

    similar_parents = get_similar_parent_ideas(db, vdb, embedding_id)

    random_children = get_random_children_from_parents(similar_parents)

    uids = [cid["uid"] for cid in random_children]

    users_dict = fetch_users(uids)

    child_ideas_processed = []

    for child_idea in random_children:
        uid = child_idea["uid"]
        user = users_dict[uid]

        child_idea_processed = {
            "id": child_idea["id"],
            "path": child_idea["path"],
            "title": child_idea["title"],
            "description": child_idea["description"],
            "emoji": child_idea["emoji"],
            "children": child_idea["children"],
            "uid": child_idea["uid"],
            "userPhotoUrl": user["photoUrl"],
            "userHandle": user["handle"],
        }

        child_ideas_processed.append(child_idea_processed)

    return child_ideas_processed


# similar_parents =
# [['C2Px9cRW5vbmD7mZ9ArX_0', 4.018357276916504],
# ['KpEiykeXiDwQoB3gCEBW_0', 0.0],
# ['KywCb8RqySJkUoxjulOu_0', 1.4454364776611328],
# ['PjKOLexLCGtxOqTeXzGh_0_1', 3.6773252487182617]]
def get_similar_parent_ideas(db: Session, vdb: Milvus, embedding_id: str):

    vector_id = fetch_vector_id(db, embedding_id)
    if not vector_id:
        return []

    result_vectors = get_by_id(vdb, vector_id)  # length is always 1

    search_vectors_res_dict = search_vectors(vdb, result_vectors)

    sv_ids = list(search_vectors_res_dict.keys())
    sv_ids_near = [
        svid
        for svid in sv_ids
        if search_vectors_res_dict[svid] <= L2_DISTANCE_THRESHOLD
    ]

    embedding_docs_dict = {}
    embeddings = fetch_embedding_ids(db, sv_ids_near)

    for embedding in embeddings:
        embedding_docs_dict[embedding.vector_id] = embedding.embedding_id

    similar_search_res = []

    for vector_id, embedding_id in embedding_docs_dict.items():
        distance = search_vectors_res_dict[vector_id]
        similar_search_res.append([embedding_id, distance])

    return similar_search_res


def get_random_children_from_parents(similar_parents):
    if not similar_parents:
        return []

    embedding_ids = [item[0] for item in similar_parents]

    parent_doc_ids = []
    for embedding_id in embedding_ids:
        parts = embedding_id.split("_")
        parent_doc_ids.append(parts[0])

    parent_doc_ids = list(set(parent_doc_ids))

    root_ideas_dict = fetch_ideas(parent_doc_ids)

    child_ideas = []

    for item in similar_parents:
        embedding_id = item[0]
        parts = embedding_id.split("_")

        doc_id = parts[0]
        child_path = [int(path_id) for path_id in parts[1:]]

        curr = root_ideas_dict[doc_id]
        curr_children = []

        if child_path == [0]:
            curr_children += curr["children"]
        else:
            for path_id in child_path[1:]:
                children = curr["children"]
                curr = children[path_id]

            curr_children += curr["children"]

        for child in curr_children:
            child["id"] = doc_id

        child_ideas += curr_children

    return child_ideas
