from fastapi import APIRouter, Request, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.params import Depends

router = APIRouter()

from sqlalchemy.orm import Session
from milvus import Milvus

from dependencies import *
from db_manager import get_db, get_vdb

from services.search import get_children_ideas


@router.post("/getRemixed")
async def getRemixed(
    request: Request,
    auth_valid: bool = Depends(validate_user_auth),
    db: Session = Depends(get_db),
    vdb: Milvus = Depends(get_vdb),
):
    if not auth_valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:
        req_body = await request.json()

        if "embedding_id" not in req_body:
            raise Exception("Missing argument")

        embedding_id = req_body["embedding_id"]
        if not embedding_id:
            raise Exception("Missing argument")

        res = get_children_ideas(db, vdb, embedding_id)

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
