from backend.skills import extract_skills
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.skill_extractor import extract_skills
from pathlib import Path
import shutil
import fitz


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def extract_text_from_pdf(file_path):
    document = fitz.open(file_path)

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

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text_from_pdf(file_path)
    resume_skills = extract_skills(resume_text)

    skills = extract_skills(resume_text)

    return {
    "message": "Resume uploaded and analyzed successfully",
    "filename": file.filename,
    "extracted_text": resume_text,
    "extracted_skills": resume_skills
}