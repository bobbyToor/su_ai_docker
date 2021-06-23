from firebase_admin import firestore
from common.config import (
    FIRESTORE_USERS_COLLECTION,
    FIRESTORE_IDEAS_COLLECTION,
    FIRESTORE_EMBEDDINGS_COLLECTION,
)

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

    if not embedding_id or not isinstance(embedding_id, str):
        return None

    doc_snap = (
        client.collection(FIRESTORE_EMBEDDINGS_COLLECTION).document(embedding_id).get()
    )

    if not doc_snap.exists:
        return None

    doc_dict = doc_snap.to_dict()

    if "vector_id" not in doc_dict:
        raise Exception("vector_id not found in document for : ", embedding_id)

    vector_id = doc_dict["vector_id"]
    return int(vector_id)


def fetch_embedding_ids(vector_ids):
    if not vector_ids:
        return {}

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


def fetch_ideas(idea_ids):

    if not idea_ids:
        return {}

    idea_ids = list(set(idea_ids))

    idea_doc_refs = [
        client.collection(FIRESTORE_IDEAS_COLLECTION).document(id) for id in idea_ids
    ]

    docs = client.get_all(idea_doc_refs)

    res_dict = {}

    for doc in docs:
        res_dict[doc.id] = doc.to_dict()

    return res_dict


def fetch_users(uids):
    uids = list(set(uids))

    uid_doc_refs = [
        client.collection(FIRESTORE_USERS_COLLECTION).document(id) for id in uids
    ]

    docs = client.get_all(uid_doc_refs)

    res_dict = {}

    for doc in docs:
        res_dict[doc.id] = doc.to_dict()

    return res_dict


# def on_snapshot(doc_snapshot, changes, read_time):
#     for change in changes:
#         if change.type.name == "ADDED":
#             print(f"New city: {change.document.id}")
#         elif change.type.name == "MODIFIED":
#             print(f"Modified city: {change.document.id}")
#         elif change.type.name == "REMOVED":
#             print(f"Removed city: {change.document.id}")


# doc_ref = client.collection(FIRESTORE_IDEAS_COLLECTION)
# doc_watch = doc_ref.on_snapshot(on_snapshot)
