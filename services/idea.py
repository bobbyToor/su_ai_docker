import logging as logger

# logger.basicConfig(level=logger.INFO)

from services.dbs.milvus_db import (
    insert_vectors,
    delete_vectors,
    drop_collection,
    init_table_milvus,
)
from services.dbs.mysql_db import (
    create_table_mysql,
    get_vector_ids,
    insert_embeddings,
    delete_embeddings,
    delete_table,
)

from services.dbs.firestore_db import fetch_ideas, fetch_all_ideas
from services.embedder import get_title_embeddings
from common.config import MILVUS_COLLECTION


def insert_idea(doc_id):
    logger.info(f"Inserting idea : {doc_id}")

    # check if idea already exists
    # then delete it
    delete_idea(doc_id)

    # now insert new one
    # generate embeddings based on titles only (for now)
    ideas_dict = fetch_ideas([doc_id])
    doc_data = ideas_dict[doc_id]
    title_embeddings = get_title_embeddings(doc_id, doc_data)

    vectors = [v.tolist() for v in list(title_embeddings.values())]
    embedding_ids = list(title_embeddings.keys())

    # create vector ids
    status, vector_ids = insert_vectors(MILVUS_COLLECTION, vectors)
    logger.info(f"insert_vectors status : {status}")

    values = []
    for i, vid in enumerate(vector_ids):
        eid = embedding_ids[i]
        values.append([doc_id, vid, eid])

    # inserts vector ids into mysql
    insert_embeddings(values)


def delete_idea(doc_id):
    logger.info(f"Deleting idea : {doc_id}")

    # get vector_ids
    vector_ids = get_vector_ids(doc_id)
    logger.info(f"vector_ids to delete for idea : {doc_id}, {vector_ids}")

    if not vector_ids:
        return None

    # delete old embeddings from mysql
    delete_embeddings(doc_id)
    logger.info(f"Deleted vector_ids from mysql : {vector_ids}")

    # delete old vectors(if any) from vector db
    status = delete_vectors(MILVUS_COLLECTION, vector_ids)
    logger.info(f"Delete idea from milvus: {doc_id}, status : {status}")

    return status


def sync():
    logger.info(f"Syncing now ....")

    drop_collection()
    logger.info(f"Dropped milvus collection")
    delete_table()
    logger.info(f"Dropped mysql table")

    init_table_milvus()
    create_table_mysql()

    vectors = []
    data_dict = {}

    tuple_list = []

    docs_dict = fetch_all_ideas()

    for doc_id, doc_data in docs_dict.items():
        data_dict[doc_id] = {}
        title_embeddings = get_title_embeddings(doc_id, doc_data)

        doc_embeddings = list(title_embeddings.keys())

        doc_vectors = [v.tolist() for v in list(title_embeddings.values())]
        vectors += doc_vectors

        for index, doc_embedding in enumerate(doc_embeddings):
            tuple_list.append((doc_id, doc_vectors[index], doc_embedding))

    docs_dict.clear()

    # create vector ids
    status, vector_ids = insert_vectors(MILVUS_COLLECTION, vectors)
    logger.info(f"insert_vectors status : {status}")

    data_list = []

    for index, vid in enumerate(vector_ids):
        vector = vectors[index]

        for (doc_id, doc_vector, doc_embedding) in tuple_list:
            if vector == doc_vector:
                data_list.append([doc_id, vid, doc_embedding])

    tuple_list.clear()

    # inserts vector ids into mysql
    insert_embeddings(data_list)
    logger.info(f"total embeddings inserted : {len(data_list)}")
