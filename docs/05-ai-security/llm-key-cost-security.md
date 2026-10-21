# LLM API Key and Cost Security in Laravel

> Last reviewed: 2026-10. Applies to: PHP 8.4+, Laravel 11.x – 13.x.

## Quick Answer

LLM cost security protects applications from financial denial-of-wallet attacks and credential leaks. In Laravel, API keys must remain strictly server-side (stored in encrypted environment configurations, never bundled into frontend assets). Every AI endpoint requires granular per-tenant token budgets, strict sliding-window rate limiting via Redis, and automatic circuit breakers that halt traffic when unexpected token spikes occur.

## Threat Model

- **Attacker Profile**: Malicious actors exploiting public endpoints, compromised customer accounts, or bots conducting high-frequency LLM generation loops.
- **Attack Vectors**:
  - **Exposed Keys**: Committing OpenAI/Anthropic/Google keys in Git or exposing them in frontend Vue/Inertia props.
  - **Denial-of-Wallet (Billing Attack)**: Looping high-context prompt requests with maximum `max_tokens` set to drain enterprise API quotas.
  - **Noisy Neighbor Tenant**: A single tenant overwhelming a shared API tier, causing service failure for all other customers.
- **Impact & Cost**: Thousands of dollars in unbudgeted cloud invoices, account suspension by AI providers, and application downtime.

## Vulnerable Example

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class VulnerableAiChatController extends Controller
{
    /**
     * [INSECURE]: No rate limiting, unbounded token limits, and keys loaded directly from raw env.
     */
    public function chat(Request $request)
    {
        // Vulnerable: no user quota check, no maximum token constraint
        $prompt = (string) $request->input('message');

        $response = Http::withToken((string) env('OPENAI_API_KEY'))
            ->post('https://api.openai.com/v1/chat/completions', [
                'model' => 'gpt-4o',
                'messages' => [['role' => 'user', 'content' => $prompt]],
            ]);

        return response()->json($response->json());
    }
}
```

## Secure Implementation

```php
<?php

declare(strict_types=1);

namespace App\Services\Ai;

use App\Models\User;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use RuntimeException;

final class SecureLlmBillingGuardService
{
    private const int DAILY_USER_TOKEN_LIMIT = 50_000;
    private const int MAX_OUTPUT_TOKENS = 1_000;

    /**
     * [SECURE]: Budget verification, enforced output limits, and usage tracking.
     */
    public function executeBudgetedPrompt(User $user, string $systemPrompt, string $userMessage): string
    {
        $todayKey = 'ai_usage:' . $user->id . ':' . now()->format('Y-m-d');
        $usedTokens = (int) Cache::get($todayKey, 0);

        if ($usedTokens >= self::DAILY_USER_TOKEN_LIMIT) {
            Log::warning('User exceeded daily AI token quota', [
                'user_id' => $user->id,
                'used_tokens' => $usedTokens,
            ]);
            throw new RuntimeException('Daily AI token quota reached. Please upgrade or try again tomorrow.');
        }

        $apiKey = config('services.openai.key');
        if (!is_string($apiKey) || empty($apiKey)) {
            throw new RuntimeException('OpenAI API key is missing or not configured.');
        }

        $response = Http::withToken($apiKey)
            ->timeout(20)
            ->post('https://api.openai.com/v1/chat/completions', [
                'model' => 'gpt-4o-mini',
                'max_tokens' => self::MAX_OUTPUT_TOKENS, // Enforce strict upper bound
                'messages' => [
                    ['role' => 'system', 'content' => $systemPrompt],
                    ['role' => 'user', 'content' => $userMessage],
                ],
            ]);

        if (!$response->successful()) {
            Log::error('AI Provider Error', ['status' => $response->status(), 'body' => $response->body()]);
            throw new RuntimeException('Upstream AI service error.');
        }

        $totalUsedInCall = (int) $response->json('usage.total_tokens', 500);

        // Atomically update user daily token usage
        Cache::increment($todayKey, $totalUsedInCall);
        Cache::put($todayKey, Cache::get($todayKey), now()->endOfDay());

        return (string) $response->json('choices.0.message.content');
    }
}
```

## Laravel-Specific Notes

- **Configuration Caching**: Always reference `config('services.openai.key')` rather than `env()`. In production, `php artisan config:cache` prevents `env()` calls from returning null.
- **Middleware Rate Limiting**: In `bootstrap/app.php`, configure a custom rate limiter:
  ```php
  RateLimiter::for('ai-endpoints', function (Request $request) {
      return Limit::perMinute(10)->by($request->user()?->id ?: $request->ip());
  });
  ```
- **Webhook Spend Alerts**: Set hard monthly spending caps directly inside your OpenAI/Anthropic organization console.

## Checklist

- [ ] API keys are stored in `.env` and accessed strictly through `config(...)` (never passed to frontend).
- [ ] Every LLM request specifies an explicit `max_tokens` parameter.
- [ ] Endpoints are protected by rate limiting in `bootstrap/app.php`.
- [ ] Token usage is recorded and checked against per-user or per-organization daily spend caps.
- [ ] Hard billing caps and automated alerts are configured in the AI provider dashboard.

## Further Reading

- [OWASP Top 10 for LLM Applications (LLM04: Model Denial of Service)](https://genai.owasp.org/llm-top-10/)
- [Laravel Cache & Atomic Locks Documentation](https://laravel.com/docs/13.x/cache)
- [Laravel Rate Limiting Documentation](https://laravel.com/docs/13.x/routing#rate-limiting)
