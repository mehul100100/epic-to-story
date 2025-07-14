from fastapi import FastAPI
from app.api.v1.endpoints import router as v1_router
from app.core.config import settings
import uvicorn

app = FastAPI(
    title="Epic to Story Generator",
    description="A LangGraph-based FastAPI service to convert epics into detailed user stories.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)