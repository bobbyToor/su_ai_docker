from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("paraphrase-distilroberta-base-v1")
# model = SentenceTransformer("paraphrase-TinyBERT-L6-v2")
# model = SentenceTransformer("bert-base-nli-mean-tokens")
model = SentenceTransformer("paraphrase-mpnet-base-v2")

# cos_sim = util.pytorch_cos_sim(emb1, emb1 + emb2)

# print("Cosine-Similarity:", cos_sim)


def get_id_embeddings(doc_id, doc_data):
    id_title_dict = get_id_titles(doc_id, doc_data, {})

    title_embeddings = {}

    for id, title in id_title_dict.items():
        title_embeddings[id] = model.encode(title)

    return title_embeddings


def get_id_titles(doc_id, doc_data, id_title_dict):

    title = doc_data["title"]
    path = doc_data["path"]
    children = doc_data["children"]

    joined_path = "_".join(str(path_id) for path_id in path)
    joined_id = doc_id + "_" + joined_path

    id_title_dict[joined_id] = title

    for child in children:
        get_id_titles(doc_id, child, id_title_dict)

    return id_title_dict
