import logging
from services.dbs.milvus_db import insert_vectors
from services.dbs.firestore_db import get_idea_doc_data, insert_ids
from services.embedder import get_id_embeddings
from common.config import MILVUS_COLLECTION


def insert_data(doc_id):

    try:

        doc_data = get_idea_doc_data(doc_id)
        id_embeddings = get_id_embeddings(doc_id, doc_data)

        vectors = [v.tolist() for v in list(id_embeddings.values())]
        idea_ids = list(id_embeddings.keys())

        status, milvus_ids = insert_vectors(MILVUS_COLLECTION, vectors)
        insert_ids(milvus_ids, idea_ids)

        return status

    except Exception as e:
        print(e, 1)
        logging.error(e)
        return "Error with {}".format(e)
