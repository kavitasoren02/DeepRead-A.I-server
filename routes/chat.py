from fastapi import APIRouter, Request, Depends, HTTPException
from utils.jwthandler import get_current_user
from utils.gemini_summarizer import get_summary_from_text
from models.recordsCollection import Record
from db import file_collection, records_collection
from datetime import datetime

router = APIRouter()


@router.post("/chat/summary")
async def chat_summary(request: Request, user_id: str = Depends(get_current_user)):
    body = await request.json()
    session_id = body.get("session_id")
    prompt = body.get("prompt")

    if not session_id or not prompt:
        raise HTTPException(status_code=400, detail="Missing sessionId and prompt")

    # Fetch file content if exists
    file_data = file_collection.find_one({"session_id": session_id})
    if not file_data:
        raise HTTPException(status_code=404, detail="Session ID not found")

    extracted_text = file_data.get("extracted_text", "")
    full_text = f"{extracted_text}\n{prompt}"

    # Store user message
    user_doc = Record(
        sessionId=session_id,
        userId=user_id,
        message=prompt,
        isAIgenerated=False,
        timeStamp=datetime.utcnow()
    )
    records_collection.insert_one(user_doc.dict())

    # Generate AI summary
    summary = get_summary_from_text(full_text)

    # Store AI message
    ai_doc = Record(
        sessionId=session_id,
        userId=user_id,
        message=summary,
        isAIgenerated=True,
        timeStamp=datetime.utcnow()
    )
    records_collection.insert_one(ai_doc.dict())

    return {
        "sessionId": session_id,
        "userId": ai_doc.userId,
        "message": ai_doc.message,
        "isAIgenerated": ai_doc.isAIgenerated,
        "audioPath": "",
        "timeStamp": ai_doc.timeStamp
    }

@router.get("/chat/{session_id}")
async def fetch_chat_history(session_id: str, user_id: str = Depends(get_current_user)):
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session_id")

    docs = list(records_collection.find({"sessionId": session_id}).sort("timeStamp", 1))
    if not docs:
        raise HTTPException(status_code=404, detail="No chat history found for this session")

    history = [
        {
            "sessionId": doc["sessionId"],
            "userId": doc["userId"],
            "message": doc["message"],
            "isAIgenerated": doc["isAIgenerated"],
            "audioPath": doc["audioPath"],
            "timeStamp": doc["timeStamp"]
        }
        for doc in docs
    ]

    return history

@router.get("/history")
async def fetch_history(user_id: str = Depends(get_current_user)):
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$group": {"_id": "$sessionId", "chat": {"$first": "$$ROOT"}}},
        {"$sort": {"timeStamp": -1}},
        {"$project": {
            "sessionId": "$_id",
            "_id": 0,
            "chat": {
                **{
                    k: {"$toString": "$chat." + k} if k == "_id" else f"$chat.{k}"
                    for k in ["_id", "sessionId", "userId", "message", "isAIgenerated", "audioPath", "timeStamp"]
                }
            }
        }}
    ]

    result = list(records_collection.aggregate(pipeline))

    return result