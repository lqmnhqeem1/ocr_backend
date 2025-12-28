import os
import base64
from io import BytesIO
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from fastapi import HTTPException

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

if not AZURE_ENDPOINT or not AZURE_KEY:
    raise ValueError("Azure credentials not found")

client = DocumentIntelligenceClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_KEY)
)

async def extract_text_from_base64_pdf(file_name: str, base64_pdf: str):
    if not file_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        pdf_bytes = base64.b64decode(base64_pdf)
        pdf_stream = BytesIO(pdf_bytes)

        poller = client.begin_analyze_document(
            "prebuilt-read",
            pdf_stream
        )

        result = poller.result()

        ocr_pages = []

        # ✅ Preferred: pages (if available)
        if result.pages:
            for page in result.pages:
                lines = []
                if page.lines:
                    lines = [line.content for line in page.lines]

                ocr_pages.append({
                    "page": page.page_number,
                    "text": "\n".join(lines)
                })

        # ✅ Fallback: full document content
        elif result.content:
            ocr_pages.append({
                "page": 1,
                "text": result.content
            })

        else:
            raise HTTPException(
                status_code=500,
                detail="OCR completed but no text content returned"
            )

        return {
            "file_name": file_name,
            "pages": len(ocr_pages),
            "ocr_text": ocr_pages,
            "ocr_length": len(base64_pdf)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )
