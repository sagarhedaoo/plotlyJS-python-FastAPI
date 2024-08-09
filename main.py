

from fastapi import FastAPI, Query
import redis
import requests
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import gzip
from fastapi.responses import JSONResponse, StreamingResponse

load_dotenv()

app = FastAPI()

origins = ["http://localhost:3000", "https://192.168.1.193:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis(host="localhost", port=6379, db=0)

CACHE_EXPIRATION = 3600


@app.get("/getData2")
async def get_data():
    API_URL = os.getenv("SCHEMA2_URL")
    cache_key = "plot_data"
    cached_data = r.get(cache_key)

    if cached_data:
        print("Returning cached data")
        data = json.loads(cached_data)
    else:
        print("Fetching new data from API")
        response = requests.get(API_URL)
        data = response.json()
        r.setex(cache_key, CACHE_EXPIRATION, json.dumps(data))

    return data


# uvicorn main:app --reload
