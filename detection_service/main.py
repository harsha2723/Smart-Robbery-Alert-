from fastapi import FastAPI, UploadFile, BackgroundTasks
from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio

# Initialize FastAPI app
app = FastAPI()

# MongoDB Configuration
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["security_system"]

# Beanie Document Model
class IncidentLog(Document):
    timestamp: datetime
    description: str
    video_path: str

@app.on_event("startup")
async def init_db():
    await init_beanie(database=db, document_models=[IncidentLog])

# Simulate Motion Detection (Concurrency Example)
async def detect_motion(file: UploadFile):
    await asyncio.sleep(3)  # Simulate processing
    print(f"Motion detected in file: {file.filename}")

@app.post("/upload-video/")
async def upload_video(file: UploadFile, background_tasks: BackgroundTasks):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Background task for detection
    background_tasks.add_task(detect_motion, file)
    
    # Log incident
    log = IncidentLog(
        timestamp=datetime.now(),
        description="Motion detected",
        video_path=file_path,
    )
    await log.insert()

    return {"status": "Processing", "file_path": file_path}

@app.get("/incident-logs/")
async def get_incident_logs():
    logs = await IncidentLog.find_all().to_list()
    return logs
