from typing import List
from sqlalchemy.orm import Session
from models import *


def fetch_vector_id(db: Session, embedding_id: str):
    embedding = (
        db.query(Embedding).filter(Embedding.embedding_id == embedding_id).first()
    )

    if embedding:
        return embedding.vector_id
    return None


def fetch_embedding_ids(db: Session, vector_ids: List[str]):
    embeddings = db.query(Embedding).filter(Embedding.vector_id.in_(vector_ids)).all()
    return embeddings


def insert_embeddings(db: Session, embeddings: List[Embedding]):
    db.bulk_save_objects(embeddings)
    db.commit()


def delete_embeddings_by_idea_id(db: Session, idea_id: str):
    db.query(Embedding).filter(Embedding.idea_id == idea_id).delete(
        synchronize_session=False
    )
    db.commit()


def get_embeddings_by_idea_id(db: Session, idea_id: str):
    embeddings = db.query(Embedding).filter(Embedding.idea_id == idea_id).all()
    return embeddings
