from typing import List
from sqlalchemy.orm import Session
from models.user import User


class CRUDUser:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def fetch_by_id(self, uid: str):
        user = self.db_session.query(User).filter(User.id == uid).first()
        return user

    def fetch_by_ids(self, uids: List[str]):
        users = self.db_session.query(User).filter(User.id.in_(uids)).all()
        return users

    def bulk_save(self, users: List[User]):
        self.db_session.bulk_save_objects(users)
        self.db_session.commit()
