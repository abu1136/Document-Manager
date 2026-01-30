from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.exc import OperationalError
import os
import time

from app.database import engine, Base
from app.routers import auth, documents, admin, profile

app = FastAPI(title="Document Manager")


# ===============================
# STARTUP — WAIT FOR MYSQL
# ===============================
@app.on_event("startup")
def startup():
    for attempt in range(15):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected")
            break
        except OperationalError:
            print("Waiting for MySQL...")
            time.sleep(3)
    else:
        raise RuntimeError("MySQL not available")

    # Ensure required folders
    os.makedirs("files", exist_ok=True)
    os.makedirs("files/letterhead", exist_ok=True)
    os.makedirs("files/COMP/DOC", exist_ok=True)


# ===============================
# ROUTERS
# ===============================
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)
app.include_router(profile.router)


# ===============================
# STATIC UI
# ===============================
app.mount("/ui", StaticFiles(directory="frontend/ui", html=True), name="ui")


# ===============================
# FILE DOWNLOAD
# ===============================
@app.get("/files/{file_path:path}")
def download_file(file_path: str):
    full_path = os.path.join("files", file_path)
    if not os.path.exists(full_path):
        return {"error": "File not found"}
    return FileResponse(full_path)
