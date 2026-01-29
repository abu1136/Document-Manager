from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import auth, documents, admin

app = FastAPI(title="Document Manager")

# API routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)

# Serve generated documents
app.mount("/files", StaticFiles(directory="files"), name="files")

# Serve frontend UI
app.mount(
    "/ui",
    StaticFiles(directory="frontend/ui", html=True),
    name="ui"
)
