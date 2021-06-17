# import logging

from services.dbs.milvus_db import drop_collection
from services.search import search_similar
from services.insert import insert_data
import uvicorn
from fastapi import Request, FastAPI
import firebase_admin

credentials = firebase_admin.credentials.Certificate(
    "./common/su-city-firebase-adminsdk-rpzgp-49b35ca454.json"
)
firebase_admin.initialize_app(
    credentials, {
        "databaseURL": "https://su-city-default-rtdb.firebaseio.com/"}
)


app = FastAPI()


@app.get("/")
def hello():
    return {"Hello": "World"}


@app.post("/submitIdea")
async def submitIdea(request: Request):
    req_body = await request.json()
    doc_id = req_body["id"]

    status = insert_data(doc_id)

    return status


@app.post("/getSimilar")
async def getSimilar(request: Request):
    req_body = await request.json()
    embedding_id = req_body["embedding_id"]

    embedding_ids = search_similar(embedding_id)

    return embedding_ids


@app.get("/dropCollection")
async def dropCollection():
    res = drop_collection()
    return res


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=3001)
