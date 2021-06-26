import uvicorn
import logging as logger

logger.basicConfig(level=logger.INFO)

from dotenv import load_dotenv

load_dotenv()

import firebase_admin

credentials = firebase_admin.credentials.Certificate("./common/service_account.json")
firebase_admin.initialize_app(credentials)

from fastapi import FastAPI

fastapp = FastAPI()


@fastapp.on_event("startup")
def startup():
    logger.info("App started")


@fastapp.on_event("shutdown")
def shutdown():
    logger.warning("App shutting down")


from routers import idea, remix, admin

fastapp.include_router(idea.router)
fastapp.include_router(remix.router)
fastapp.include_router(admin.router)


if __name__ == "__main__":
    uvicorn.run(app=fastapp, host="0.0.0.0", port=3001)
