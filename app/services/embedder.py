from sentence_transformers import SentenceTransformer
import uuid

# model = SentenceTransformer("paraphrase-distilroberta-base-v1")
# model = SentenceTransformer("paraphrase-TinyBERT-L6-v2")
# model = SentenceTransformer("bert-base-nli-mean-tokens")
model = SentenceTransformer("paraphrase-mpnet-base-v2")


def get_idea_data_list(doc_id, doc_data):
    ideas_list = []
    traverse_add_ideas(doc_id, None, doc_data, ideas_list)
    return ideas_list


def traverse_add_ideas(doc_id, parent_id, doc_data, idea_list):

    current_id = uuid.uuid4().hex

    title = doc_data["title"]
    title_vector = model.encode(title)

    idea_list.append(
        {
            "id": current_id,
            "fid": doc_id,
            "parent_id": parent_id,
            "title": title,
            "title_vector": title_vector,
            "uid": doc_data["uid"],
            "description": doc_data["description"],
            "emoji": doc_data["emoji"],
            "is_public": doc_data["isPublic"],
            "created_at": doc_data["createdAt"],
            "updated_at": doc_data["updatedAt"],
            # "path": current_path,
        }
    )

    children = doc_data["children"]
    for child in children:
        traverse_add_ideas(doc_id, current_id, child, idea_list)

    # idea.embedding_id = embedding_id
