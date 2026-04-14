# services/auth_service.py
from fastapi import HTTPException
from db.users import users_db          

def verify_user(username: str, password: str) -> dict:
    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}