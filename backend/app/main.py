from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.endpoints import upload, debug
import logging

# Set debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Bank Statement Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["analysis"])
app.include_router(debug.router, prefix="/api", tags=["debug"])

@app.get("/")
def root():
    return {"message": "Bank Statement Analyzer API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
