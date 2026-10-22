---
name: first-feature
description: Guide for scaffolding a new protected API endpoint with BOLA, BFLA, and strict schema validation.
---

# First Feature Skill: Scaffolding a Secure Protected API Endpoint

## Overview
Add a new resource `/api/v1/invoices/{invoice_id}` adhering strictly to OWASP API Security Top 10 principles.

## Implementation Guide

### 1. Define Request & Response Schemas
```python
from pydantic import BaseModel, Field

class InvoiceResponse(BaseModel):
    invoice_id: str
    amount: float
    status: str
    owner_id: str

    model_config = {"extra": "forbid"}
```

### 2. Implement Endpoint with BOLA Protection
```python
@app.get("/api/v1/invoices/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: str, current_user: UserContext = Depends(get_current_user)):
    invoice = db.get_invoice(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # BOLA Protection Check
    if invoice.owner_id != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="BOLA protection: Access forbidden")
        
    return invoice
```

### 3. Write Unit Test
```python
def test_invoice_bola_prevention(client):
    attacker_token = make_token("user-attacker")
    resp = client.get("/api/v1/invoices/inv-100", headers={"Authorization": f"Bearer {attacker_token}"})
    assert resp.status_code == 403
    assert "BOLA protection" in resp.json()["detail"]
```
