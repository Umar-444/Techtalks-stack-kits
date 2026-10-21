# Laravel Security Best Practices — Laravel 13

> **Requirements:** Laravel 11 minimum, **Laravel 13 recommended**. Laravel 10 reached EOL on February 4, 2025 — do not use in production.

## Authentication & Authorization

Laravel 13 provides a robust, modern security foundation. Use the official starter kits for authentication scaffolding.

### Installing API Authentication (Laravel 13)

```bash
# Install Sanctum via artisan (Laravel 11+ replaces manual setup)
php artisan install:api

# This publishes migrations, config, and sets up Sanctum automatically
```

### Middleware Registration — `bootstrap/app.php` (Laravel 11+)

> Warning: **`app/Http/Kernel.php` was removed in Laravel 11.** All middleware must now be registered in `bootstrap/app.php`.

```php
<?php
// bootstrap/app.php — Laravel 13 way
use App\Http\Middleware\SecurityHeaders;
use App\Http\Middleware\ForceHttps;
use Illuminate\Foundation\Application;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        api: __DIR__.'/../routes/api.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (\Illuminate\Foundation\Configuration\Middleware $middleware) {
        // Global middleware (runs on every request)
        $middleware->append(SecurityHeaders::class);
        $middleware->append(ForceHttps::class);

        // Named middleware aliases
        $middleware->alias([
            'role' => \App\Http\Middleware\CheckRole::class,
            'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
        ]);

        // API middleware group
        $middleware->api(append: [
            \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
        ]);
    })
    ->withExceptions(function (\Illuminate\Foundation\Configuration\Exceptions $exceptions) {
        $exceptions->renderable(function (\Throwable $e, $request) {
            if ($request->expectsJson()) {
                return response()->json(['error' => 'Server error'], 500);
            }
        });
    })
    ->create();
```

### Key Features in Laravel 13

| Feature | Description |
|---|---|
| `install:api` artisan command | One-command Sanctum API setup |
| Enhanced `Rate::` facade | Named rate limiters with per-user scoping |
| `Precognition` | Real-time validation before form submission |
| `Model::preventSilentlyDiscardingAttributes()` | Throws exception on unguarded mass-assignment |
| `withoutOverlapping()` | Prevents concurrent job execution |
| Improved `Health` checks | Built-in `/up` endpoint for deployment monitoring |

## Mass Assignment Protection

Laravel protects against mass assignment vulnerabilities. Always use `$fillable` — never `$guarded = []`.

```php
<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    // [SECURE] Explicit allowlist
    protected $fillable = ['name', 'email', 'password'];

    // [INSECURE] NEVER do this — mass assignment vulnerability
    // protected $guarded = [];
}
```

## SQL Injection Prevention

- Eloquent ORM automatically parameterizes queries
- Use Query Builder methods — never concatenate raw SQL
- Always bind parameters in raw queries

```php
<?php
// [SECURE] Eloquent — auto-escaped
$user = User::where('email', $email)->first();

// [SECURE] Query Builder — parameterized
$users = DB::table('users')
    ->where('role', $role)
    ->where('active', true)
    ->get();

// [SECURE] Raw query with binding (when needed)
$results = DB::select('SELECT * FROM users WHERE email = ?', [$email]);

// [INSECURE] NEVER — SQL injection vulnerability
$results = DB::select("SELECT * FROM users WHERE email = '$email'");
```

## Cross-Site Scripting (XSS) Protection

- Blade `{{ }}` auto-escapes all output — use it by default
- Only use `{!! !!}` for **trusted, sanitized** HTML content
- Implement strict CSP with nonces (see [Secure Headers](SecureHeaders.md))

```blade
{{-- Safe — auto-escaped --}}
{{ $user->name }}

{{-- Warning: Only for pre-sanitized HTML (use with caution) --}}
{!! $sanitizedHtml !!}

{{-- Blade components auto-escape attributes --}}
<x-user-card :name="$user->name" />
```

## Encrypted Model Attributes (Store Secrets at Rest)

```php
<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class UserProfile extends Model
{
    protected $fillable = ['user_id', 'ssn', 'api_key', 'notes'];

    protected function casts(): array
    {
        return [
            // Automatically encrypted/decrypted using APP_KEY
            'ssn'     => 'encrypted',
            'api_key' => 'encrypted',
            'settings' => 'encrypted:array', // Encrypted JSON
        ];
    }
}
```

## File Storage Security

```php
<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class FileController extends Controller
{
    public function upload(Request $request)
    {
        $request->validate([
            'document' => [
                'required',
                'file',
                'max:10240',                          // 10MB max
                'mimes:pdf,docx,xlsx',               // MIME allowlist
                'mimetypes:application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            ],
        ]);

        // Cryptographically random filename — prevents enumeration
        $filename = Str::random(40) . '.' . $request->file('document')->getClientOriginalExtension();

        // Store in private disk (outside web root)
        $path = $request->file('document')->storeAs('documents', $filename, 'private');

        return response()->json(['path' => $path]);
    }

    public function download(string $filename)
    {
        // Authorization check first
        $this->authorize('download', $filename);

        // Serve from private storage — not publicly accessible
        return Storage::disk('private')->download('documents/' . $filename);
    }
}
```

## API Security with Laravel Sanctum 4.x

```php
<?php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        $request->validate([
            'email'    => ['required', 'email:rfc,dns'],
            'password' => ['required', 'string', 'min:15'],
            'device'   => ['required', 'string', 'max:255'],
        ]);

        if (!Auth::attempt($request->only('email', 'password'))) {
            throw ValidationException::withMessages([
                'email' => ['Invalid credentials.'],
            ]);
        }

        $user = $request->user();

        // Revoke all previous tokens for this device
        $user->tokens()->where('name', $request->device)->delete();

        // Create scoped token
        $token = $user->createToken(
            name: $request->device,
            abilities: ['read', 'write'],
            expiresAt: now()->addDays(30),
        );

        return response()->json([
            'token' => $token->plainTextToken,
            'type'  => 'Bearer',
            'expires_at' => $token->accessToken->expires_at,
        ]);
    }

    public function logout(Request $request)
    {
        // Revoke current token
        $request->user()->currentAccessToken()->delete();

        return response()->json(['message' => 'Logged out successfully']);
    }
}
```

## Rate Limiting (Laravel 13 `Rate::` Facade)

```php
<?php
// routes/api.php — Laravel 13 named rate limiters
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('api', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(120)->by($request->user()->id)   // Authenticated: 120/min
        : Limit::perMinute(20)->by($request->ip());          // Guest: 20/min
});

RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(5)->by($request->ip()),
        Limit::perMinute(10)->by($request->input('email')),
    ];
});
```

## Environment Security

```php
// .env — production essentials
APP_ENV=production
APP_DEBUG=false          // Warning: NEVER true in production
APP_KEY=base64:...       // Must be set — used for encryption

// Laravel 13: use secrets manager for sensitive values
// AWS SSM: APP_KEY=${ssm:/myapp/prod/app_key}
// HashiCorp Vault: APP_KEY=${vault:secret/myapp/app_key}
```

## Security Middleware (Laravel 13)

```php
<?php
// bootstrap/app.php — complete security middleware setup
->withMiddleware(function ($middleware) {
    // Enforce HTTPS in production
    if (app()->isProduction()) {
        $middleware->append(\Illuminate\Http\Middleware\TrustProxies::class);
    }

    // Prevent clickjacking, set security headers
    $middleware->append(\App\Http\Middleware\SecurityHeaders::class);

    // CSRF — enabled for web, excluded for API (uses token auth)
    $middleware->web(append: [
        \App\Http\Middleware\VerifyCsrfToken::class,
    ]);
})
```

## Database Security

```php
<?php
// config/database.php — MySQL TLS connection
'mysql' => [
    'driver'    => 'mysql',
    'host'      => env('DB_HOST'),
    'database'  => env('DB_DATABASE'),
    'username'  => env('DB_USERNAME'),
    'password'  => env('DB_PASSWORD'),
    'charset'   => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'options'   => [
        // [SECURE] Encrypted DB connection
        PDO::MYSQL_ATTR_SSL_CA      => env('DB_SSL_CA'),
        PDO::MYSQL_ATTR_SSL_VERIFY_SERVER_CERT => true,
        PDO::ATTR_EMULATE_PREPARES  => false,  // Disable emulated prepares
        PDO::ATTR_STRINGIFY_FETCHES => false,
    ],
],
```

## Laravel 13 EOL Schedule (Reference)

| Version | Status | EOL Date |
|---|---|---|
| Laravel 13 | [SECURE] Current | August 2027 (security: Feb 2028) |
| Laravel 12 | [SECURE] Active LTS | February 2027 (security: Feb 2028) |
| Laravel 11 | [SECURE] Supported | September 2026 |
| Laravel 10 | [INSECURE] EOL | February 4, 2025 |
| Laravel 9 | [INSECURE] EOL | February 8, 2024 |
