from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api_azure_document_ocr.router import router as azuredoc_router

app = FastAPI(title="OCR Backend API")

# Allow CORS for frontend (replace "*" with your frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Azure OCR router
app.include_router(azuredoc_router)
