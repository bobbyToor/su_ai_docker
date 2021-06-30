from sentence_transformers import SentenceTransformer
from models import Idea
import uuid

# model = SentenceTransformer("paraphrase-distilroberta-base-v1")
# model = SentenceTransformer("paraphrase-TinyBERT-L6-v2")
# model = SentenceTransformer("bert-base-nli-mean-tokens")
model = SentenceTransformer("paraphrase-mpnet-base-v2")

# cos_sim = util.pytorch_cos_sim(emb1, emb1 + emb2)

# print("Cosine-Similarity:", cos_sim)

# returns
# {"dadas_0_1": [1231,312331,33], "dadas_0_2": [123,76,776,7]}
# arrays are np arrays
# def get_title_embeddings(doc_id, doc_data):
#     id_title_dict = get_id_titles(doc_id, doc_data, {})

#     title_embeddings = {}

#     for embedding_id, title in id_title_dict.items():
#         title_embeddings[embedding_id] = model.encode(title)

#     return title_embeddings


# returns
# {"dadas_0_1": "make a oizza", "dadas_0_2": "add topping"}
# def get_id_titles(doc_id, doc_data, id_title_dict):

#     title = doc_data["title"]
#     path = doc_data["path"]
#     children = doc_data["children"]

#     joined_path = "_".join(str(path_id) for path_id in path)
#     joined_id = doc_id + "_" + joined_path

#     id_title_dict[joined_id] = title

#     for child in children:
#         get_id_titles(doc_id, child, id_title_dict)

#     return id_title_dict


def get_idea_data_list(doc_id, doc_data):
    ideas_list = []
    traverse_add_ideas(doc_id, None, doc_data, ideas_list)
    return ideas_list


def traverse_add_ideas(doc_id, parent_path, doc_data, idea_list):

    # idea = Idea()
    current_id = uuid.uuid4().hex
    if not parent_path:
        current_path = f"{current_id}"
    else:
        current_path = f"{parent_path},{current_id}"

    title = doc_data["title"]
    title_vector = model.encode(title)

    idea_list.append(
        {
            "id": current_id,
            "fid": doc_id,
            "title": title,
            "title_vector": title_vector,
            "uid": doc_data["uid"],
            "description": doc_data["description"],
            "emoji": doc_data["emoji"],
            "is_public": doc_data["isPublic"],
            "created_at": doc_data["createdAt"],
            "updated_at": doc_data["updatedAt"],
            "path": current_path,
        }
    )

    children = doc_data["children"]
    for child in children:
        traverse_add_ideas(doc_id, current_path, child, idea_list)

    # idea.embedding_id = embedding_id
