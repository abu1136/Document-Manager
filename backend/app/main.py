import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database import Base, engine

# Import models so SQLAlchemy registers tables
from app.models.user import User
from app.models.letterhead import Letterhead
from app.models.document import Document

# Routers
from app.routers import auth, documents, admin, profile

app = FastAPI(title="Document Manager")


# -------------------------
# DB wait + auto-migration
# -------------------------
@app.on_event("startup")
def startup():
    max_retries = 10
    delay = 2  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            break
        except OperationalError:
            print(f"Waiting for database... ({attempt}/{max_retries})")
            time.sleep(delay)
    else:
        raise RuntimeError("Database not available after retries")

    # Safe auto-migration
    Base.metadata.create_all(bind=engine)


# -------------------------
# Routers
# -------------------------
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)
app.include_router(profile.router)


# -------------------------
# Static files
# -------------------------
app.mount("/files", StaticFiles(directory="files"), name="files")
app.mount("/ui", StaticFiles(directory="frontend/ui", html=True), name="ui")
