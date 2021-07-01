import logging as logger
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.params import Depends

from crud.crud_idea import CRUDIdea
from milvus import Milvus
from api.dependencies import get_idea_crud, get_user_crud, get_vdb, validate_admin
from db.utils import *
from services.idea.sync import sync
from db.milvus_db import drop_collection, init_table_milvus

router = APIRouter()


@router.get("/")
def hello():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"Hello": "World"},
    )


@router.get("/sync")
async def sync_dbs(
    crud_idea: CRUDIdea = Depends(get_idea_crud),
    crud_user: CRUDIdea = Depends(get_user_crud),
    vdb: Milvus = Depends(get_vdb),
    auth_valid: bool = Depends(validate_admin),
):
    if not auth_valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:

        sync(crud_idea, crud_user, vdb)

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


@router.get("/clearData")
async def dropCollection(
    vdb: Milvus = Depends(get_vdb),
    auth_valid: bool = Depends(validate_admin),
):
    if not auth_valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:

        drop_collection(vdb)
        logger.info(f"Dropped milvus collection")

        drop_tables()
        logger.info(f"Dropped mysql tables")

        init_table_milvus(vdb)
        create_tables()

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
