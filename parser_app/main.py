import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from pathlib import Path

current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir.parent / 'task2'))
sys.path.append(str(current_dir.parent))

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from async_parser import parser
from worker.celery_config import celery_app
from celery.result import AsyncResult

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Initializing parser')
    await parser.initialize()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/parse")
async def parse_single_url(url: str):
    try:
        return await parser.parse_url(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/parse_async")
async def parse_async(url: str):
    task = celery_app.send_task("parse_url_task", args=[url])
    
    return {
        "task_id": task.id,
        "status": "accepted"
    }
    
@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None,
    }