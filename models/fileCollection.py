from pydantic import BaseModel

class FileUpload(BaseModel):
    user_id: str
    session_id: str
    extracted_text: str