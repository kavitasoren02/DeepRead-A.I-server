from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Record(BaseModel):
    sessionId: str
    userId: str
    message: str
    isAIgenerated: bool
    audioPath: Optional[str]= None
    timeStamp:  datetime = Field(default_factory=datetime.utcnow)