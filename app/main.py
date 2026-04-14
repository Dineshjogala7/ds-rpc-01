from fastapi import FastAPI, Depends
from schemas import LoginResponse, ChatRequest, ChatResponse
from utils.auth import authenticate
from services.rag_service import get_rag_response

app = FastAPI()

# Login endpoint
@app.get("/login", response_model=LoginResponse)        
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


# Test endpoint
@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)        
def chat(request: ChatRequest, user=Depends(authenticate)):   
    answer = get_rag_response(query=request.message, role=user["role"])
    return {
        "username": user["username"],
        "role":     user["role"],
        "query":    request.message,      
        "answer":   answer
    }