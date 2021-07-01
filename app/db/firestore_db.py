from firebase_admin import firestore
from core.config import (
    FIRESTORE_USERS_COLLECTION,
    FIRESTORE_IDEAS_COLLECTION,
)

client = firestore.client()


def fetch_all_ideas():

    docs = client.collection(FIRESTORE_IDEAS_COLLECTION).stream()

    res_dict = {}

    for doc in docs:
        res_dict[doc.id] = doc.to_dict()

    return res_dict


def fetch_all_users():

    docs = client.collection(FIRESTORE_USERS_COLLECTION).stream()

    res_dict = {}

    for doc in docs:
        res_dict[doc.id] = doc.to_dict()

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
    if not uids:
        return {}

    uids = list(set(uids))

    uid_doc_refs = [
        client.collection(FIRESTORE_USERS_COLLECTION).document(id) for id in uids
    ]

    docs = client.get_all(uid_doc_refs)

    res_dict = {}

    for doc in docs:
        res_dict[doc.id] = doc.to_dict()

    return res_dict
