from crud.crud_user import CRUDUser
import logging as logger
from typing import Generator
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from fastapi.params import Depends
import secrets
from firebase_admin import auth
from db.config import SessionLocal

from db.milvus_db import get_milvus_client
from milvus import Milvus
from crud.crud_idea import CRUDIdea

from core.config import (
    ADMIN_USERNAME,
    ADMIN_PASSWORD,
)

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)

    return correct_username and correct_password


def validate_user_auth(token: str = Depends(oauth2_scheme)):
    try:
        auth.verify_id_token(token)
        return True
    except Exception as e:
        logger.warning(e)
        return False


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_vdb() -> Milvus:
    return get_milvus_client()


def get_idea_crud() -> CRUDIdea:
    db_session = next(get_db())
    yield CRUDIdea(db_session)


def get_user_crud() -> CRUDUser:
    db_session = next(get_db())
    yield CRUDUser(db_session)
