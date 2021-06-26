import logging as logger

from sqlalchemy.orm import Session


from services.dbs.milvus_db import *
from services.dbs.sql_crud import *
from models import *
from db_manager import delete_embeddings_table, create_embeddings_table

from services.dbs.firestore_db import fetch_all_ideas
from services.embedder import get_title_embeddings
from common.config import MILVUS_COLLECTION


def sync(db: Session, vdb: Milvus):
    logger.info(f"Syncing now ....")

    drop_collection(vdb)
    logger.info(f"Dropped milvus collection")
    delete_embeddings_table()
    logger.info(f"Dropped mysql table")

    init_table_milvus(vdb)
    create_embeddings_table()

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
    status, vector_ids = insert_vectors(vdb, MILVUS_COLLECTION, vectors)
    logger.info(f"insert_vectors status : {status}")

    embeddings = []

    for index, vid in enumerate(vector_ids):
        vector = vectors[index]

        for (doc_id, doc_vector, doc_embedding) in tuple_list:
            if vector == doc_vector:

                embedding = Embedding()
                embedding.vector_id = vid
                embedding.embedding_id = doc_embedding
                embedding.idea_id = doc_id

                embeddings.append(embedding)

    tuple_list.clear()

    # inserts vector ids into mysql
    insert_embeddings(db, embeddings)
    logger.info(f"total embeddings inserted : {len(embeddings)}")
