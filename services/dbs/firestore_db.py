from firebase_admin import firestore
from common.config import FIRESTORE_IDEAS_COLLECTION, FIRESTORE_EMBEDDINGS_COLLECTION

client = firestore.client()


def get_idea_doc_data(doc_id):
    snapshot = client.collection(FIRESTORE_IDEAS_COLLECTION).document(doc_id).get()
    data = snapshot.to_dict()
    return data


def insert_ids(milvus_ids, embedding_ids):
    batch = client.batch()

    for index, milvus_id in enumerate(milvus_ids):
        embedding_id = embedding_ids[index]

        doc_ref = client.collection(FIRESTORE_EMBEDDINGS_COLLECTION).document(
            embedding_id
        )

        batch.set(doc_ref, {"vector_id": str(milvus_id)})

    batch.commit()


def fetch_vector_id(embedding_id):
    doc_ref = client.collection(FIRESTORE_EMBEDDINGS_COLLECTION).document(embedding_id)
    doc_dict = doc_ref.get().to_dict()
    vector_id = doc_dict["vector_id"]

    return int(vector_id)


def fetch_embedding_ids(vector_ids):
    vector_ids = [str(vid) for vid in vector_ids]

    docs = (
        client.collection(FIRESTORE_EMBEDDINGS_COLLECTION)
        .where("vector_id", "in", vector_ids)
        .stream()
    )

    res_dict = {}
    for doc in docs:
        vector_id = int(doc.to_dict()["vector_id"])
        res_dict[vector_id] = doc.id

    return res_dict
