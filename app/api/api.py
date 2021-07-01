from fastapi import APIRouter
from api.endpoints import idea, remix, admin

api_router = APIRouter()

api_router.include_router(idea.router)
api_router.include_router(remix.router)
api_router.include_router(admin.router)
