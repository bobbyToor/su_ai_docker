import logging as log
from services.dbs.firestore_db import fetch_vector_id, fetch_embedding_ids
from services.dbs.milvus_db import get_by_id, search_vectors
from common.config import L2_DISTANCE_THRESHOLD


def search_similar(embedding_id):
    try:

        vector_id = fetch_vector_id(embedding_id)
        result_vectors = get_by_id(vector_id)

        search_vectors_res_dict = search_vectors(result_vectors)

        sv_ids = list(search_vectors_res_dict.keys())
        sv_ids_near = [
            svid
            for svid in sv_ids
            if search_vectors_res_dict[svid] <= L2_DISTANCE_THRESHOLD
        ]

        embedding_docs_dict = fetch_embedding_ids(sv_ids_near)

        similar_search_res = []

        for vector_id, embedding_id in embedding_docs_dict.items():
            distance = search_vectors_res_dict[vector_id]
            similar_search_res.append([embedding_id, distance])

        return similar_search_res

    except Exception as e:
        log.error(e)
        return "Error with {}".format(e)
