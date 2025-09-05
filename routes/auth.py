from fastapi import APIRouter, HTTPException, Response, Request
from models.userCollection import User
from models.userCollection import Login
from db import users_collection
from utils.hashing import hash_password,verify_password
from utils.jwthandler import create_access_token, verify_access_token
from bson import ObjectId


router = APIRouter()

@router.post("/register")
def register_user(user: User):
    if users_collection.find_one({"email" : user.email}):
        raise HTTPException(status_code=400, msg="User already exsists")
    
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)

    users_collection.insert_one(user_dict)
    return{"msg": "User registered successfully"}


@router.post("/login")
def login_user(login: Login, response: Response):
    user = users_collection.find_one({"email": login.email})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(login.password ,user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    token_data = {
        "email": user["email"],
        "user_id": str(user["_id"]),
    }

    jwt_token = create_access_token(token_data)

    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,
        samesite="Lax"
    )
    
    return {"msg": "Login successful"}


@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"msg": "Logout Successful"}



@router.get("/info")
def info(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_access_token(token)
     
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = users_collection.find_one({"_id": ObjectId(payload["user_id"])})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return {"msg": "User info", "user": user}
