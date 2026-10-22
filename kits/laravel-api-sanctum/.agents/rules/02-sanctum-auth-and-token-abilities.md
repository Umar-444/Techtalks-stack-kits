# 02 Sanctum Auth And Token Abilities

# Rule 02: Sanctum Auth & Token Abilities

- User model must include the `Laravel\Sanctum\HasApiTokens` trait.
- Tokens must be issued with explicit ability lists:
  ```php
  $token = $user->createToken('device-name', ['projects:read', 'projects:write']);
  ```
- Protect write endpoints with `middleware('ability:projects:write')`.
- Plaintext tokens are returned strictly once upon generation; never re-display or persist plaintext tokens in logs.
- Logouts must explicitly delete `$request->user()->currentAccessToken()`.
- Enforce token expiration in `config/sanctum.php` or `AuthServiceProvider::boot()`.
