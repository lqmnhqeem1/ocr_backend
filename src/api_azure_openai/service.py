import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2025-04-01-preview"
    )

def structure_ocr_text(ocr_text: str) -> dict:
    """
    Uses Azure OpenAI to convert raw OCR text into structured fields and tables.
    Returns STRICT JSON.
    """

    response = client.chat.completions.create(
        model="gpt-5-mini",
        max_completion_tokens=3000,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an OCR data structuring expert. "
                    "Convert OCR text into structured data. "
                    "Return STRICT JSON only. "
                    "Do not calculate, normalize, or guess values."
                ),
            },
            {
                "role": "user",
                "content": f"""
Convert the following OCR text into structured JSON with:
- fields (key-value pairs)
- tables (table_name, columns, rows)
- notes (optional)

OCR TEXT:
<<<
{ocr_text}
>>>
""",
            },
        ],
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Azure OpenAI returned invalid JSON")
