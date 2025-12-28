from fastapi import APIRouter
from pydantic import BaseModel
from src.api_azure_document_ocr.service import extract_text_from_base64_pdf

router = APIRouter(prefix="/azuredoc-ocr", tags=["AzureDocOCR"])

class Base64PDFRequest(BaseModel):
    file_name: str
    base64_pdf: str

@router.post("/base64")
async def ocr_base64(request: Base64PDFRequest):
    """
    Accepts a PDF as a base64 string and returns OCR result as JSON.
    """
    result = await extract_text_from_base64_pdf(request.file_name, request.base64_pdf)
    return result
