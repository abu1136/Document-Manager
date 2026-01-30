from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import engine, Base
from app.routers import auth, documents, admin, profile

import os

app = FastAPI(title="Document Manager")


# ===============================
# STARTUP – AUTO DB MIGRATION
# ===============================
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
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
# FILE DOWNLOADS
# ===============================
@app.get("/files/{file_path:path}")
def download_file(file_path: str):
    full_path = os.path.join("files", file_path)

    if not os.path.exists(full_path):
        return {"error": "File not found"}

    return FileResponse(full_path, filename=os.path.basename(full_path))
