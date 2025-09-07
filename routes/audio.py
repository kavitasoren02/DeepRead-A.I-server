from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends, Form
from utils.audio_to_text import audio_to_text
from utils.text_to_audio import text_to_audio
from utils.gemini_summarizer import get_summary_from_text
from utils.jwthandler import get_current_user
from db import file_collection
import tempfile
import os
import shutil
import uuid
from models.recordsCollection import Record
from db import file_collection, records_collection
from datetime import datetime

router = APIRouter()

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

@router.post("/audio_summary")
async def audio_summary(
    session_id: str = Form(...),
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session_id")
    
    file_data = file_collection.find_one({
        "session_id": session_id
    })
    
    if not file_data:
        raise HTTPException(status_code=404, detail="Session ID not found")

    extracted_text = file_data.get("extracted_text", "")

    # Generate unique file name
    file_extension = os.path.splitext(file.filename)[-1] or ".mp3"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    audio_path = os.path.join(AUDIO_DIR, unique_filename)

    # Save uploaded file to audio folder
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert speech to text
    transcribed_text = audio_to_text(audio_path)

    user_doc = Record(
        sessionId=session_id,
        userId=user_id,
        message=transcribed_text,
        isAIgenerated=False,
        audioPath=unique_filename,
        timeStamp=datetime.utcnow()
    )
    records_collection.insert_one(user_doc.dict())

    # Merge old + new text
    full_text = f"{extracted_text} {transcribed_text}".strip()

    # Generate summary
    summary = get_summary_from_text(full_text)

    # Convert summary text into audio
    summary_audio_path = text_to_audio(summary)

    ai_doc = Record(
        sessionId=session_id,
        userId=user_id,
        message=summary,
        isAIgenerated=True,
        audioPath=summary_audio_path,
        timeStamp=datetime.utcnow()
    )
    records_collection.insert_one(ai_doc.dict())

    return {
        "sessionId": session_id,
        "userId": ai_doc.userId,
        "message": ai_doc.message,
        "isAIgenerated": ai_doc.isAIgenerated,
        "audioPath": summary_audio_path,
        "timeStamp": ai_doc.timeStamp
    }