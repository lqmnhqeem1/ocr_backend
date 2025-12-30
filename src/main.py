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


if __name__ == "__main__":
    # Launch the FastAPI app when executed as a module (python -m src.main)
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
