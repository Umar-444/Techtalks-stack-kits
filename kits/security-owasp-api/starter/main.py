import ipaddress
import socket
import time
import urllib.parse
from collections import defaultdict
from typing import Dict, List, Optional

import jwt
from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="OWASP API Security Top 10 Reference API",
    description="Production reference implementation demonstrating automated defenses against OWASP API Security Top 10 (2023).",
    version="1.0.0",
)

SECRET_KEY = "verified-owasp-signing-key-for-development"

# In-memory mock database with tenant isolation
DOCUMENTS_DB = {
    "doc-1": {"id": "doc-1", "title": "Alice Confidential Strategy", "owner_id": "user-alice", "content": "Restricted Financials"},
    "doc-2": {"id": "doc-2", "title": "Bob Public Research", "owner_id": "user-bob", "content": "Public findings"},
}

USER_PROFILES = {
    "user-alice": {"id": "user-alice", "username": "alice", "email": "alice@example.com", "role": "admin", "internal_secret": "sensitive-data"},
    "user-bob": {"id": "user-bob", "username": "bob", "email": "bob@example.com", "role": "user", "internal_secret": "sensitive-data"},
}

RATE_LIMIT_STORE = defaultdict(list)

# Schemas
class UserContext(BaseModel):
    user_id: str
    role: str

class DocumentResponse(BaseModel):
    id: str
    title: str
    owner_id: str
    content: str

    model_config = {"extra": "forbid"}

class UserPublicProfile(BaseModel):
    id: str
    username: str
    email: str
    role: str

    model_config = {"extra": "forbid"}

class WebhookRequest(BaseModel):
    callback_url: str

# Authentication Dependency (API2:2023 Broken Authentication)
def get_current_user(request: Request) -> UserContext:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token (API2:2023)")
    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return UserContext(user_id=payload["sub"], role=payload.get("role", "user"))
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature (API2:2023)")

# Role Guard Dependency (API5:2023 Broken Function Level Authorization)
def require_admin(user: UserContext = Depends(get_current_user)) -> UserContext:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="BFLA protection: Admin privileges required (API5:2023)")
    return user

# Health endpoint
@app.get("/healthz")
def healthz():
    return {"status": "ok", "app": "security-owasp-api", "version": "1.0.0"}

# API1:2023 - Broken Object Level Authorization (BOLA)
@app.get("/api/v1/documents/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: str, current_user: UserContext = Depends(get_current_user)):
    doc = DOCUMENTS_DB.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    # Strict BOLA Check
    if doc["owner_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="BOLA protection: Forbidden access to resource (API1:2023)")
    return doc

# API3:2023 - Broken Object Property Level Authorization (BOPLA)
@app.get("/api/v1/users/{user_id}", response_model=UserPublicProfile)
def get_user_profile(user_id: str, current_user: UserContext = Depends(get_current_user)):
    profile = USER_PROFILES.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    # Response model filters out internal_secret
    return profile

# API4:2023 - Unrestricted Resource Consumption (Rate Limiting)
@app.get("/api/v1/rate-limited-action")
def rate_limited_action(current_user: UserContext = Depends(get_current_user)):
    now = time.time()
    user_requests = [t for t in RATE_LIMIT_STORE[current_user.user_id] if now - t < 60]
    if len(user_requests) >= 5:
        raise HTTPException(status_code=429, detail="API4:2023 - Rate limit exceeded. Try again in 60s.")
    user_requests.append(now)
    RATE_LIMIT_STORE[current_user.user_id] = user_requests
    return {"status": "success", "remaining_requests": 5 - len(user_requests)}

# API4:2023 - Pagination Cap
@app.get("/api/v1/documents", response_model=List[DocumentResponse])
def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    current_user: UserContext = Depends(get_current_user)
):
    user_docs = [d for d in DOCUMENTS_DB.values() if d["owner_id"] == current_user.user_id or current_user.role == "admin"]
    return user_docs[skip : skip + limit]

# API5:2023 - Broken Function Level Authorization (BFLA)
@app.delete("/api/v1/admin/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: str, admin: UserContext = Depends(require_admin)):
    if user_id in USER_PROFILES:
        del USER_PROFILES[user_id]
        return {"status": "deleted", "user_id": user_id}
    raise HTTPException(status_code=404, detail="User not found")

# API7:2023 - Server-Side Request Forgery (SSRF) Defense
@app.post("/api/v1/webhooks/verify")
def verify_webhook(webhook: WebhookRequest, current_user: UserContext = Depends(get_current_user)):
    parsed = urllib.parse.urlparse(webhook.callback_url)
    if parsed.scheme not in ["http", "https"]:
        raise HTTPException(status_code=400, detail="Invalid URL scheme. Only HTTP/HTTPS allowed.")
    
    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="Invalid URL hostname")
    
    # Block loopback, RFC1918, and cloud metadata
    try:
        ip_addr = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(ip_addr)
        if ip.is_private or ip.is_loopback or ip.is_link_local or str(ip) == "169.254.169.254":
            raise HTTPException(status_code=403, detail="SSRF protection: Outbound requests to private/cloud IPs forbidden (API7:2023)")
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="Could not resolve hostname")
        
    return {"status": "verified", "target_ip": ip_addr}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
