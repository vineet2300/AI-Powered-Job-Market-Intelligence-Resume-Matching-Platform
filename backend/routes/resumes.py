from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.skill_extractor import extract_skills
import fitz


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


def extract_text_from_pdf(pdf_bytes: bytes):
    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are allowed"
        )

    try:
        pdf_bytes = await file.read()

        if not pdf_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty"
            )

        resume_text = extract_text_from_pdf(pdf_bytes)

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from this PDF"
            )

        resume_skills = extract_skills(resume_text)

        return {
            "message": "Resume uploaded and analyzed successfully",
            "filename": file.filename,
            "extracted_text": resume_text,
            "extracted_skills": resume_skills
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process resume: {str(error)}"
        )
    