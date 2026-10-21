# PHP Security Best Practices — PHP 8.4

> **Requirements:** PHP 8.2 minimum, PHP 8.4 recommended. PHP 8.1 is EOL (November 2024) — do not use in production.

## Input Validation & Sanitization

Always validate and sanitize user input to prevent injection attacks.

### Key Principles
- Never trust user input
- Use allowlists (not blocklists) for validation
- Sanitize output based on context (HTML, JSON, SQL, shell, etc.)
- Validate data types and formats strictly

### PHP 8.4 Typed Enums for Safe Type Handling

```php
<?php
declare(strict_types=1);

// Use enums to restrict allowed values — PHP 8.1+
enum UserRole: string
{
    case Admin  = 'admin';
    case Editor = 'editor';
    case Viewer = 'viewer';
}

// Safe — only valid roles accepted
function assignRole(UserRole $role): void
{
    // $role is guaranteed to be a valid UserRole
}

assignRole(UserRole::Admin); // [SECURE] safe
assignRole('hacker');        // [INSECURE] TypeError thrown automatically
```

### PHP 8.4 — New `array_find()` for Safe Lookups

```php
<?php
declare(strict_types=1);

// PHP 8.4: array_find() — safe, no manual loops needed
$allowedExtensions = ['jpg', 'png', 'gif', 'webp'];
$uploadedExt = strtolower(pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION));

$match = array_find($allowedExtensions, fn($ext) => $ext === $uploadedExt);

if ($match === null) {
    throw new InvalidArgumentException('File type not allowed');
}
```

### PHP 8.4 — `#[\Deprecated]` Attribute for Insecure Code

```php
<?php
// Mark old insecure functions as deprecated in your codebase
#[\Deprecated(message: 'Use hashPasswordSecure() with Argon2id instead', since: '2.0')]
function hashPasswordLegacy(string $password): string
{
    return md5($password); // Never use in production
}
```

## SQL Injection Prevention

- Use prepared statements with PDO (preferred) or mysqli
- Never use string concatenation in queries
- Parameterize ALL user inputs — no exceptions

```php
<?php
declare(strict_types=1);

// [INSECURE] VULNERABLE
$query = "SELECT * FROM users WHERE email = '$email'";

// [SECURE] SECURE — PDO prepared statement
$stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
$stmt->execute([$email]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);
```

## Cross-Site Scripting (XSS) Protection

- Escape output using `htmlspecialchars()` with `ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5`
- Use Content Security Policy (CSP) with nonces — **no `unsafe-inline`**
- Validate and sanitize input
- Use Laravel's Blade `{{ }}` which auto-escapes

```php
<?php
// [SECURE] Correct — ENT_SUBSTITUTE prevents malformed UTF-8 from bypassing
echo htmlspecialchars($userInput, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5, 'UTF-8');

// [INSECURE] Weak — missing flags
echo htmlspecialchars($userInput); // susceptible to some bypasses
```

## File Upload Security

- Validate MIME types by reading file magic bytes (not just extension)
- Check file size limits before processing
- Store files **outside** the web root
- Generate cryptographically secure random filenames
- Scan for malware with ClamAV or cloud scanning APIs

```php
<?php
declare(strict_types=1);

// Read MIME type from file content, not from user-supplied data
$finfo = new finfo(FILEINFO_MIME_TYPE);
$mimeType = $finfo->file($_FILES['upload']['tmp_name']);

$allowedMimes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];

if (!in_array($mimeType, $allowedMimes, true)) {
    throw new RuntimeException('Invalid file type');
}

// Cryptographically secure filename
$filename = bin2hex(random_bytes(16)) . '.jpg';
```

## Authentication & Authorization

- Use `password_hash()` with `PASSWORD_ARGON2ID` (OWASP 2024 recommendation)
- Minimum password length: **15 characters** (NIST SP 800-63B 2024)
- Implement Passkeys/WebAuthn as the preferred passwordless option
- Use HTTPS everywhere — TLS 1.3 preferred
- Implement rate limiting and account lockout
- Log all authentication events to structured logs

```php
<?php
declare(strict_types=1);

// [SECURE] OWASP 2024 — Argon2id parameters
$hash = password_hash($password, PASSWORD_ARGON2ID, [
    'memory_cost' => 65536, // 64MB minimum
    'time_cost'   => 3,     // 3 iterations (OWASP 2024)
    'threads'     => 1,     // 1 thread (recommended for web)
]);

// [SECURE] Always use password_verify() — timing-safe
if (password_verify($inputPassword, $hash)) {
    // authenticated
}

// [SECURE] Rehash on login if parameters have changed
if (password_needs_rehash($hash, PASSWORD_ARGON2ID, ['memory_cost' => 65536, 'time_cost' => 3, 'threads' => 1])) {
    $newHash = password_hash($password, PASSWORD_ARGON2ID, ['memory_cost' => 65536, 'time_cost' => 3, 'threads' => 1]);
    // Update hash in database
}
```

## Error Handling

- Never expose stack traces, SQL errors, or file paths in production
- Use custom error pages (`APP_DEBUG=false` in production)
- Log errors to structured log files (Monolog/Sentry), never to the browser
- Handle all exceptions — use a top-level exception handler

```php
<?php
declare(strict_types=1);

set_exception_handler(function (Throwable $e): void {
    // Log full error internally
    error_log(sprintf('[%s] %s in %s:%d', get_class($e), $e->getMessage(), $e->getFile(), $e->getLine()));

    // Return generic message to user
    http_response_code(500);
    echo json_encode(['error' => 'An internal server error occurred.']);
    exit;
});
```

## Configuration Security

- Store ALL secrets in environment variables — never in code
- Use secrets managers (HashiCorp Vault, AWS SSM, Azure Key Vault) in production
- Restrict file permissions: `640` for configs, `750` for directories
- Keep all dependencies updated — run `composer audit --locked` in CI/CD

```bash
# Run daily in CI/CD
composer audit --locked

# Check for known vulnerabilities
composer outdated --direct
```

## PHP 8.4 Security-Relevant New Features

| Feature | Security Benefit |
|---|---|
| `array_find()` / `array_find_key()` | Safer array lookups without manual loops |
| `#[\Deprecated]` attribute | Mark insecure code formally |
| `new` in initializers | Cleaner DI for security services |
| Asymmetric property visibility | Better encapsulation of sensitive data |
| Typed class constants | Prevents type confusion in constants |
| DOM API (HTML5 parser) | Safer HTML parsing for XSS prevention |
| BCMath object API | Safer arbitrary precision for crypto math |

## PHP EOL Schedule (Reference)

| Version | Status | EOL Date |
|---|---|---|
| PHP 8.4 | Active | November 2027 |
| PHP 8.3 | [SECURE] Security fixes | November 2026 |
| PHP 8.2 | [SECURE] Security fixes | December 2026 |
| PHP 8.1 | [INSECURE] EOL | November 25, 2024 |
| PHP 8.0 | [INSECURE] EOL | November 26, 2023 |
