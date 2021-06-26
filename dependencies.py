import logging as logger

from firebase_admin import auth

from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from fastapi.params import Depends
import secrets


from common.config import (
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
