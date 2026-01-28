from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import auth, documents, admin

app = FastAPI(title="Document Manager")

# API routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)

# Serve UI
app.mount("/ui", StaticFiles(directory="frontend/ui", html=True), name="ui")
