from dotenv import load_dotenv

load_dotenv()

import logging as logger

logger.basicConfig(level=logger.INFO)

import uvicorn
from fastapi import FastAPI

import firebase_admin

credentials = firebase_admin.credentials.Certificate("./core/service_account.json")
firebase_admin.initialize_app(credentials)

from api.api import api_router

fastapp = FastAPI()

from db.utils import init_db


@fastapp.on_event("startup")
def startup():

    init_db()
    logger.info("App started")


@fastapp.on_event("shutdown")
def shutdown():
    logger.warning("App shutting down")


fastapp.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app=fastapp, host="127.0.0.1", port=3001)
