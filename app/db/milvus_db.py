import logging
from milvus import *
from core.config import (
    MILVUS_HOST,
    MILVUS_PORT,
    METRIC_TYPE,
    MILVUS_COLLECTION,
    VECTOR_DIMENSION,
    TOP_K,
)


def get_milvus_client():
    milvus_client = Milvus(host=MILVUS_HOST, port=MILVUS_PORT)
    return milvus_client


def create_collection_milvus(milvus_client, collection_name, dimension):
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
        logging.error(e)


def create_index(milvus_client):
    param = {"nlist": 16384}
    try:
        status = milvus_client.create_index(
            MILVUS_COLLECTION, IndexType.IVF_FLAT, param
        )
        return status
    except Exception as e:
        logging.error(e)


def init_table_milvus(milvus_client):
    _, collections = milvus_client.list_collections()

    if MILVUS_COLLECTION not in collections:
        print(f"Creating milvus collection - {MILVUS_COLLECTION}")
        create_collection_milvus(milvus_client, MILVUS_COLLECTION, VECTOR_DIMENSION)
        create_index(milvus_client)


def total_count(milvus_client):
    try:
        _, result = milvus_client.count_entities(MILVUS_COLLECTION)
        return result
    except Exception as e:
        logging.error(e)


def insert_vectors(milvus_client, vectors):

    # create index before every insert
    create_index(milvus_client)

    try:
        status, ids = milvus_client.insert(
            collection_name=MILVUS_COLLECTION,
            records=vectors,
        )

        # milvus_client.flush([MILVUS_COLLECTION])
        # no need as of now as it does it
        # automatically after every 1s

        return status, ids
    except Exception as e:
        logging.error(e)


def delete_vectors(milvus_client, collection_name, ids):
    if not ids:
        return None

    try:
        status = milvus_client.delete_entity_by_id(collection_name, ids)

        return status
    except Exception as e:
        logging.error(e)


def get_by_id(milvus_client, milvus_id):
    if not milvus_id:
        return [[]]

    try:
        _, result_vectors = milvus_client.get_entity_by_id(
            MILVUS_COLLECTION, [milvus_id]
        )

        return result_vectors
    except Exception as e:
        logging.error(e)


def search_vectors(milvus_client, vectors):

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


def drop_collection(milvus_client):
    status = milvus_client.drop_collection(MILVUS_COLLECTION)
    milvus_client.flush([MILVUS_COLLECTION])
    return status
