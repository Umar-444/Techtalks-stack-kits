---
id: 03-bfla-and-role-rbac
title: Broken Function Level Authorization (BFLA) and RBAC Enforcement
globs: "starter/**/*.py,tests/**/*.py"
alwaysApply: true
---

# Broken Function Level Authorization (BFLA) and RBAC Enforcement

## 1. Declarative Role Guarding
- Protect administrative, financial, and operational routes with explicit dependency injection:
  ```python
  def require_role(required_role: str):
      def role_checker(user: UserContext = Depends(get_current_user)):
          if user.role != required_role:
              raise HTTPException(
                  status_code=status.HTTP_403_FORBIDDEN,
                  detail="BFLA protection: Insufficient role permissions"
              )
          return user
      return role_checker
  ```

## 2. HTTP Method Symmetry
- Verify authorization on every HTTP verb independently. A user authorized to execute `GET /api/v1/users/{id}` must not automatically inherit `DELETE /api/v1/users/{id}` or `PUT /api/v1/users/{id}`.

## 3. Scope & Capability Verification
- For machine-to-machine tokens, inspect OAuth2 scopes (`read:reports`, `write:payments`) in addition to role tags.
