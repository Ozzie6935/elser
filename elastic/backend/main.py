from fastapi import FastAPI
from app import router

app = FastAPI(
    title="Elasticsearch Search API",
    description="A FastAPI application for searching Elasticsearch using ELSER (semantic), fuzzy, or keyword search.",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Elasticsearch Search API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 