import logging as logger

from fastapi import APIRouter, Request, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.params import Depends
from crud.crud_idea import CRUDIdea
from milvus import Milvus
from api.dependencies import get_idea_crud, get_user_crud, get_vdb, validate_user_auth
from services.search import get_children_ideas

router = APIRouter()


@router.post("/getRemixed")
async def getRemixed(
    request: Request,
    crud_idea: CRUDIdea = Depends(get_idea_crud),
    crud_user: CRUDIdea = Depends(get_user_crud),
    vdb: Milvus = Depends(get_vdb),
    auth_valid: bool = Depends(validate_user_auth),
):
    # if not auth_valid:
    #     return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="🤐")

    try:
        req_body = await request.json()

        if "idea_id" not in req_body:
            raise Exception("Missing argument")

        idea_id = req_body["idea_id"]
        if not idea_id:
            raise Exception("Missing argument")

        res = get_children_ideas(crud_idea, crud_user, vdb, idea_id)

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
