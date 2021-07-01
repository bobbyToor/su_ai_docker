from typing import List
from sqlalchemy.orm import Session
from models.idea import Idea


class CRUDIdea:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def fetch_by_id(self, idea_id: str):
        idea = self.db_session.query(Idea).filter(Idea.id == idea_id).first()
        return idea

    def fetch_by_fid(self, fid: str):
        ideas = self.db_session.query(Idea).filter(Idea.fid == fid).all()
        return ideas

    def fetch_by_vector_ids(self, vector_ids: List[str]):
        ideas = self.db_session.query(Idea).filter(Idea.vector_id.in_(vector_ids)).all()
        return ideas

    def get_1st_children(self, parents: List[Idea]):
        parent_ids = [idea.id for idea in parents]
        ideas = self.db_session.query(Idea).filter(Idea.parent_id.in_(parent_ids)).all()
        return ideas

    def insert_embedded_ideas(self, embedded_ideas: List[Idea]):
        self.db_session.bulk_save_objects(embedded_ideas)
        self.db_session.commit()

    def mark_delete_ideas_by_fid(self, fid: str):
        self.db_session.query(Idea).filter(Idea.fid == fid).update(
            {"deleted": True}, synchronize_session=False
        )
        self.db_session.commit()
