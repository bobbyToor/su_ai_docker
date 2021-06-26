from fastapi import APIRouter, Request, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.params import Depends

router = APIRouter()

from sqlalchemy.orm import Session
from milvus import Milvus

from dependencies import *
from db_manager import get_db, get_vdb


from services.idea.insert import insert_idea
from services.idea.delete import delete_idea
from services.idea.sync import sync


@router.put("/idea")
async def write_idea(
    request: Request,
    auth_valid: bool = Depends(validate_admin),
    db: Session = Depends(get_db),
    vdb: Milvus = Depends(get_vdb),
):
    if not auth_valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:
        req_body = await request.json()

        if "id" not in req_body:
            raise Exception("Missing argument")

        doc_id = req_body["id"]
        if not doc_id:
            raise Exception("Missing argument")

        insert_idea(db, vdb, doc_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "🤩"},
        )
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)},
        )


@router.delete("/idea")
async def delete_idea_request(
    request: Request,
    auth_valid: bool = Depends(validate_admin),
    db: Session = Depends(get_db),
    vdb: Milvus = Depends(get_vdb),
):
    if not auth_valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:
        req_body = await request.json()

        if "id" not in req_body:
            raise Exception("Missing argument")

        doc_id = req_body["id"]

        delete_idea(db, vdb, doc_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "🤩"},
        )
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": e.to_dict()},
        )


@router.get("/sync")
async def sync_dbs(
    auth_valid: bool = Depends(validate_admin),
    db: Session = Depends(get_db),
    vdb: Milvus = Depends(get_vdb),
):
    if not auth_valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:
        sync(db, vdb)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "🤩"},
        )

    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )
