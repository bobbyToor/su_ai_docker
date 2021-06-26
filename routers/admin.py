from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.params import Depends

router = APIRouter()

from sqlalchemy.orm import Session

from dependencies import *
from milvus import Milvus

from db_manager import delete_embeddings_table, create_embeddings_table, get_vdb

from services.dbs.milvus_db import drop_collection, init_table_milvus


@router.get("/")
def hello():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"Hello": "World"},
    )


@router.get("/clearData")
async def dropCollection(
    auth_valid: bool = Depends(validate_admin),
    vdb: Milvus = Depends(get_vdb),
):
    if not auth_valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:
        drop_collection(vdb)
        delete_embeddings_table()

        init_table_milvus(vdb)
        create_embeddings_table()

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
