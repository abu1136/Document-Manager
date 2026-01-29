from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

# Import models so SQLAlchemy knows them
from app.models.user import User
from app.models.letterhead import Letterhead
from app.models.document import Document

# Import routers
from app.routers import auth, documents, admin, profile

app = FastAPI(title="Document Manager")

# -------------------------
# Automatic DB migration
# -------------------------
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# -------------------------
# API Routers
# -------------------------
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)
app.include_router(profile.router)


# -------------------------
# Static file serving
# -------------------------

# Generated documents (PDF / DOCX)
app.mount(
    "/files",
    StaticFiles(directory="files"),
    name="files"
)

# Frontend UI
app.mount(
    "/ui",
    StaticFiles(directory="frontend/ui", html=True),
    name="ui"
)
