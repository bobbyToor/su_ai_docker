import logging
from milvus import *
from common.config import (
    MILVUS_HOST,
    MILVUS_PORT,
    METRIC_TYPE,
    MILVUS_COLLECTION,
    VECTOR_DIMENSION,
    TOP_K,
)

milvus_client = Milvus(host=MILVUS_HOST, port=MILVUS_PORT)


def init_table():
    _, collections = milvus_client.list_collections()

    if MILVUS_COLLECTION not in collections:
        print(f"Creating collection - {MILVUS_COLLECTION}")
        create_collection_milvus(MILVUS_COLLECTION, VECTOR_DIMENSION)
        create_index()


def create_collection_milvus(collection_name, dimension):
    try:
        collection_param = {
            "collection_name": collection_name,
            "dimension": dimension,
            "index_file_size": 2048,
            "metric_type": METRIC_TYPE,
        }
        status = milvus_client.create_collection(collection_param)
        return status
    except Exception as e:
        print("Milvus ERROR:", e)
        logging.error(e)


def create_index():
    param = {"nlist": 16384}
    try:
        status = milvus_client.create_index(
            MILVUS_COLLECTION, IndexType.IVF_FLAT, param
        )
        return status
    except Exception as e:
        print("Milvus ERROR:", e)
        logging.error(e)


def insert_vectors(collection_name, vectors):
    init_table()

    try:
        status, ids = milvus_client.insert(
            collection_name=collection_name,
            records=vectors,
        )

        create_index()
        milvus_client.flush([MILVUS_COLLECTION])

        return status, ids
    except Exception as e:
        print("Milvus ERROR:", e)
        logging.error(e)


def get_by_id(milvus_id):
    if not milvus_id:
        return [[]]

    try:
        _, result_vectors = milvus_client.get_entity_by_id(
            MILVUS_COLLECTION, [milvus_id]
        )

        return result_vectors
    except Exception as e:
        logging.error(e)


def search_vectors(vectors):

    if vectors == [[]]:
        return {}

    try:
        _, res = milvus_client.search(
            collection_name=MILVUS_COLLECTION,
            query_records=vectors,
            top_k=TOP_K,
            params={"nprobe": 32},
        )

        res_dict = {}
        for sv in res[0]:
            res_dict[sv.id] = sv.distance

        return res_dict

    except Exception as e:
        logging.error(e)


def drop_collection():
    status = milvus_client.drop_collection(MILVUS_COLLECTION)
    milvus_client.flush([MILVUS_COLLECTION])
    return status
