from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends, Form
from utils.audio_to_text import audio_to_text
from utils.text_to_audio import text_to_audio
from utils.gemini_summarizer import get_summary_from_text
from utils.jwthandler import get_current_user
from db import file_collection
import tempfile

router = APIRouter()

@router.post("/audio_summary")
async def audio_summary(
    session_id: str = Form(...),
    file: UploadFile = File(...),
):
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session_id")
    
    file_data = file_collection.find_one({
        "session_id": session_id
    })

    if not file_data:
        raise HTTPException(status_code=404, detail="Session ID not found")
    extracted_text= file_data.get("extracted_text", "")

    temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    with open(temp_audio_path, "wb") as f:
        f.write(await file.read())

    transcribed_text = audio_to_text(temp_audio_path)

    # full_text = f"{extracted_text}\n{transcribed_text}"
    full_text = f"{extracted_text} {transcribed_text} "

    summary = get_summary_from_text(full_text)

    summary_audio_path = text_to_audio(summary)


    return {
        "message": "Summary audio created successfully",
        "session_id": session_id,
        "summary_text": summary,
        "audio_file_path": summary_audio_path
    }
            