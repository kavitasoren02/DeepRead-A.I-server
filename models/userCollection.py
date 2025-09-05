from pydantic import BaseModel, EmailStr, Field
 
class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    mobile: int = Field(..., ge=6000000000 ,le=99999999999)
    password: str

class Login(BaseModel):
    email: EmailStr
    password: str