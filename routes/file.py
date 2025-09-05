from fastapi import APIRouter, UploadFile, HTTPException, Depends
from utils.jwthandler import get_current_user
from models.fileCollection import FileUpload
from db import file_collection
import uuid;
import fitz
import shutil
import os


router = APIRouter()

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text= ""
    for page in doc:
        text += page.get_text()
    return " ".join( text.split())

@router.post("/file/upload")
def upload_file(file: UploadFile, user_id: str = Depends(get_current_user) ):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed ")
    
    session_id = str(uuid.uuid4())
    temp_file_path = f"temp_{session_id}.pdf"

    with open (temp_file_path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text = extract_text(temp_file_path)


        file_data = FileUpload(
            user_id = user_id,
            session_id = session_id,
            extracted_text = extracted_text
        )
        file_collection.insert_one(file_data.dict())
        return {
            "message": "File Uploaded successfuly",
            "user_id": user_id,
            "session_id":session_id,
            "filename": file.filename,
            "extracted_text": extracted_text,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while processing file: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)