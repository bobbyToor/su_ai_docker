import uvicorn
import logging as logger

from dotenv import load_dotenv

load_dotenv()

import secrets
from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from fastapi.params import Depends

from common.config import ADMIN_USERNAME, ADMIN_PASSWORD

import firebase_admin

credentials = firebase_admin.credentials.Certificate("./common/service_account.json")
app = firebase_admin.initialize_app(
    credentials, {"databaseURL": "https://su-city-default-rtdb.firebaseio.com/"}
)

from firebase_admin import auth

from services.insert import insert_data
from services.search import get_children_ideas
from services.dbs.milvus_db import drop_collection


app = FastAPI()

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


@app.get("/")
def hello():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"Hello": "World"},
    )


@app.post("/submitIdea")
async def submitIdea(request: Request, valid: bool = Depends(validate_admin)):
    if not valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:
        req_body = await request.json()

        if "id" not in req_body:
            raise Exception("Missing argument")

        doc_id = req_body["id"]

        res = insert_data(doc_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=str(res),
        )
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)},
        )


@app.post("/getRemixed")
async def getRemixed(request: Request, valid: bool = Depends(validate_user_auth)):
    if not valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:
        req_body = await request.json()

        if "embedding_id" not in req_body:
            raise Exception("Missing argument")

        embedding_id = req_body["embedding_id"]

        res = get_children_ideas(embedding_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=res,
        )

    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)},
        )


@app.get("/dropCollection")
async def dropCollection(valid: bool = Depends(validate_admin)):
    if not valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    res = drop_collection()
    return res


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=3001)
