from fastapi import FastAPI
from app.routers import auth, documents, admin

app = FastAPI()

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)
