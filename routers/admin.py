from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from fastapi.params import Depends

router = APIRouter()


from dependencies import *

from services.idea.sync import sync

from services.dbs.milvus_db import drop_collection, init_table_milvus


@router.get("/")
def hello():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"Hello": "World"},
    )


@router.get("/sync")
async def sync_dbs(
    request: Request,
    auth_valid: bool = Depends(validate_admin),
):
    if not auth_valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:
        dbm = request.state.dbm

        sync(dbm)

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
    request: Request,
    auth_valid: bool = Depends(validate_admin),
):
    if not auth_valid:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:

        dbm = request.state.dbm
        vdb = dbm.get_vdb()

        drop_collection(vdb)
        dbm.delete_db_tables()

        init_table_milvus(vdb)
        dbm.create_db_tables()

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
