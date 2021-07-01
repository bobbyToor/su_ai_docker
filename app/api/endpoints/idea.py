import logging as logger
from crud.crud_idea import CRUDIdea
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from fastapi.params import Depends

from milvus import Milvus

from services.idea.insert import insert_idea
from services.idea.delete import delete_idea

from api.dependencies import get_idea_crud, get_vdb, validate_admin

router = APIRouter()


@router.put("/idea")
async def write_idea(
    request: Request,
    crud_idea: CRUDIdea = Depends(get_idea_crud),
    vdb: Milvus = Depends(get_vdb),
    auth_valid: bool = Depends(validate_admin),
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

        insert_idea(crud_idea, vdb, doc_id)

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
    crud_idea: CRUDIdea = Depends(get_idea_crud),
    vdb: Milvus = Depends(get_vdb),
    auth_valid: bool = Depends(validate_admin),
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

        delete_idea(crud_idea, vdb, doc_id)

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
