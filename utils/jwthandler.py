from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Request, HTTPException

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None
    

def get_current_user(request: Request) -> str:
    token = request.cookies.get("access_token")
    # print("Token:",token)

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_access_token(token)

    if not payload or "user_id" not in payload:
        raise HTTPException(401, detail="Invalid or expired token")

    return payload["user_id"]
