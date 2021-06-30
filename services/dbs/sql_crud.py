from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_
from models import Idea


def fetch_by_id(db: Session, idea_id: str):
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    return idea


def fetch_by_idea_path(db: Session, idea_path: str):
    idea = db.query(Idea).filter(Idea.path == idea_path).first()
    return idea


def fetch_by_vector_ids(db: Session, vector_ids: List[str]):
    ideas = db.query(Idea).filter(Idea.vector_id.in_(vector_ids)).all()
    return ideas


def search_by_paths(db: Session, path_regexs: List[str]):
    filters = [Idea.path.op("regexp")(p) for p in path_regexs]
    ideas = db.query(Idea).filter(or_(*filters)).all()
    return ideas


def insert_embedded_ideas(db: Session, embedded_ideas: List[Idea]):
    db.bulk_save_objects(embedded_ideas)
    db.commit()


def mark_delete_ideas_by_fid(db: Session, fid: str):
    db.query(Idea).filter(Idea.fid == fid).update(
        {"deleted": True}, synchronize_session=False
    )
    db.commit()


def get_ideas(db: Session, fid: str):
    ideas = db.query(Idea).filter(Idea.fid == fid).all()
    return ideas
