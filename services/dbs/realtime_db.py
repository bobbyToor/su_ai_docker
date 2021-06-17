from firebase_admin import db

ref = db.reference().child("embeddings")


def insert_ids(milvus_ids, embedding_ids):

    embed_dict = {}

    for index, milvus_id in enumerate(milvus_ids):
        embedding_id = embedding_ids[index]
        embed_dict[embedding_id] = milvus_id

    ref.set(embed_dict)


def fetch_milvus_id(embedding_id):
    return ref.child(embedding_id).get()


def fetch_embedding_id(milvus_id):
    return ref.order_by_value().equal_to(milvus_id).get()
