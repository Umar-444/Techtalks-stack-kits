---
name: "sanctum-token-management"
description: "Procedures for issuing tokens, scoping abilities, managing expiration, and token revocation."
version: "1.0.0"
---

# Sanctum Token Management Skill

## Issuing Ability-Scoped Tokens
```php
$token = $user->createToken('desktop-client', [
    'projects:read',
    'projects:write',
]);
return response()->json([
    'token' => $token->plainTextToken,
    'abilities' => $token->accessToken->abilities,
]);
```

## Revoking Tokens
```php
// Revoke current token
$request->user()->currentAccessToken()->delete();

// Revoke all user tokens
$request->user()->tokens()->delete();
```
