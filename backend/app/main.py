import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database import Base, engine
from app.utils.schema_migrate import ensure_column

# Import models (table creation)
from app.models.user import User
from app.models.letterhead import Letterhead
from app.models.document import Document

# Routers
from app.routers import auth, documents, admin, profile

app = FastAPI(title="Document Manager")


@app.on_event("startup")
def startup():
    # -------- wait for DB --------
    for i in range(10):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            break
        except OperationalError:
            print(f"Waiting for database... ({i+1}/10)")
            time.sleep(2)
    else:
        raise RuntimeError("Database not reachable")

    # -------- create missing tables --------
    Base.metadata.create_all(bind=engine)

    # -------- safe column migration --------
    ensure_column(
        engine,
        table="documents",
        column="pdf_path",
        ddl="ALTER TABLE documents ADD COLUMN pdf_path VARCHAR(255)"
    )

    ensure_column(
        engine,
        table="documents",
        column="docx_path",
        ddl="ALTER TABLE documents ADD COLUMN docx_path VARCHAR(255)"
    )


# Routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)
app.include_router(profile.router)

# Static files
app.mount("/files", StaticFiles(directory="files"), name="files")
app.mount("/ui", StaticFiles(directory="frontend/ui", html=True), name="ui")
