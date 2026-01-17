import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from contextlib import asynccontextmanager
from celery.result import AsyncResult
from app.core.database import engine, Base
from app.core.celery_app import celery_app
from app.services.tasks import process_application_task

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Social Support AI Agent", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "active", "db": "postgres+qdrant+redis"}

@app.post("/submit-application")
async def submit_application(file: UploadFile = File(...), user_name: str = Form(...)):
    application_id = str(uuid.uuid4())
    file_extension = file.filename.split(".")[-1]
    file_path = f"{UPLOAD_DIR}/{application_id}.{file_extension}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    task = process_application_task.delay(application_id, [file_path])
    
    return {
        "message": "Application submitted successfully",
        "application_id": application_id,
        "task_id": task.id
    }

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    
    if task_result.ready():
        result = task_result.get()
        return {"status": "COMPLETED", "result": result}
    else:
        return {"status": "PROCESSING"}