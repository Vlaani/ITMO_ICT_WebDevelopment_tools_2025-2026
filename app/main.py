from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.router import router as api_router
from db.db import init_db

# FastAPI сказал, что event() устарел
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Initializing DB')
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api")

@app.get("/")
def hello():
    return "Hello, [username]!"