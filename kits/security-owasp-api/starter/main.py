from fastapi import FastAPI, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
import jwt
import time

app = FastAPI(title="OWASP API Security Top 10 Reference API")
SECRET_KEY = "verified-owasp-signing-key"

class UserContext(BaseModel):
    user_id: str
    role: str

def get_current_user(request: Request) -> UserContext:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token (API2:2023)")
    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return UserContext(user_id=payload["sub"], role=payload.get("role", "user"))
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token verification failed")

RESOURCES = {
    "doc-1": {"owner": "user-alice", "content": "Alice private record"},
    "doc-2": {"owner": "user-bob", "content": "Bob private record"}
}

@app.get("/api/v1/documents/{doc_id}")
def get_document(doc_id: str, user: UserContext = Depends(get_current_user)):
    doc = RESOURCES.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    if doc["owner"] != user.user_id and user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: BOLA protection triggered")
    return doc

@app.delete("/api/v1/admin/users/{target_id}")
def delete_user(target_id: str, user: UserContext = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required: BFLA protection triggered")
    return {"deleted": target_id}
