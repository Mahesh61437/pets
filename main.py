import os
import time

import uvicorn
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from fastapi import FastAPI, Request

from routers import router
from settings import settings

app = FastAPI(debug=True)
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost"]
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

load_dotenv()
ENVIRONMENT = os.getenv('DEPLOY_ENV', 'CLOUD')


# @app.on_event("startup")
# async def startup():
#     pool = await get_conn_pool()

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
