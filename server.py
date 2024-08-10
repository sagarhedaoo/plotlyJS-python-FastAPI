from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

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


@app.get("/")
async def root():
    return {"message": "Root page", "data": 0}


@app.get("/getData")
async def sample_data():
    API_URL = os.getenv("API_URL")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return JSONResponse(content=data)
    except requests.RequestException as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/getData2")
async def sample_data2():
    API_URL = os.getenv("SCHEMA2_URL")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return JSONResponse(content=data)
    except requests.RequestException as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

#uvicorn main:app --reload