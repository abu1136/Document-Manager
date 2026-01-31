from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routers import auth, documents, admin, profile
import time

app = FastAPI(title="Document Manager")

@app.on_event("startup")
def startup():
    # Wait for MySQL (increase attempts to support initial DB init)
    for _ in range(40):  # ~40 * 3s = 120s max wait
        try:
            Base.metadata.create_all(bind=engine)
            break
        except Exception as e:
            print("Waiting for MySQL...", e)
            time.sleep(3)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])

app.mount("/ui", StaticFiles(directory="frontend/ui", html=True), name="ui")
app.mount("/files", StaticFiles(directory="files"), name="files")
