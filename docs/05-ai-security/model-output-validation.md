# Model Output Validation in Laravel

> Last reviewed: 2026-10. Applies to: PHP 8.4+, Laravel 11.x – 13.x.

## Quick Answer

Model output validation treats all generated responses from an AI system as completely untrusted input. Large Language Models can hallucinate, be coerced into malicious outputs via indirect prompt injection, or generate syntax payloads designed to exploit downstream systems. Never pass LLM outputs directly into raw database queries, shell exec commands, eval functions, or unescaped Blade `{!! $output !!}` tags. Always validate schemas, type-cast fields, and escape data based on downstream context.

## Threat Model

- **Attacker Profile**: Adversaries poisoning input documents or prompts to cause second-order injection.
- **Attack Vectors**:
  - **Second-Order Cross-Site Scripting (XSS)**: An LLM generates HTML containing `<script>fetch('/steal?cookie=' + document.cookie)</script>` which is rendered via `{!! $aiOutput !!}` in Blade.
  - **Second-Order SQL Injection**: Asking a model to generate filter parameters or SQL clauses that contain malicious string escapes fed directly into `DB::raw()`.
  - **Command Injection**: An AI feature that formats file names or image resizing options passes unescaped model strings into `shell_exec()` or `proc_open()`.
- **Impact & Cost**: Complete server compromise, arbitrary code execution, database corruption, and client session hijacking.

## Vulnerable Example

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

class VulnerableAiAssistantController extends Controller
{
    /**
     * [INSECURE]: Blindly trusting AI output in database queries and Blade rendering.
     */
    public function renderAiSummary(Request $request)
    {
        $response = Http::withToken((string) config('services.openai.key'))
            ->post('https://api.openai.com/v1/chat/completions', [
                'model' => 'gpt-4o-mini',
                'messages' => [['role' => 'user', 'content' => $request->input('query')]],
            ]);

        $rawOutput = (string) $response->json('choices.0.message.content');

        // Vulnerability 1: Passing AI output into raw SQL
        DB::statement("UPDATE user_notes SET summary = '{$rawOutput}' WHERE user_id = 1");

        // Vulnerability 2: Blade template rendering rawOutput via {!! $rawOutput !!} (XSS)
        return view('notes.summary', ['summary' => $rawOutput]);
    }
}
```

## Secure Implementation

```php
<?php

declare(strict_types=1);

namespace App\Services\Ai;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Validator;
use InvalidArgumentException;
use RuntimeException;

final class SecureStructuredOutputService
{
    /**
     * [SECURE]: Uses JSON Schema Structured Outputs and validates schema strictly before use.
     *
     * @return array{sentiment: string, score: float, category: string, clean_summary: string}
     */
    public function analyzeCustomerFeedback(string $feedbackText): array
    {
        // Define strict JSON schema accepted from the LLM
        $jsonSchema = [
            'name' => 'feedback_analysis',
            'strict' => true,
            'schema' => [
                'type' => 'object',
                'properties' => [
                    'sentiment' => [
                        'type' => 'string',
                        'enum' => ['positive', 'neutral', 'negative'],
                    ],
                    'score' => [
                        'type' => 'number',
                        'description' => 'Confidence score between 0.0 and 1.0',
                    ],
                    'category' => [
                        'type' => 'string',
                        'enum' => ['billing', 'technical', 'sales', 'general'],
                    ],
                    'clean_summary' => [
                        'type' => 'string',
                        'description' => 'A 1-sentence safe plain text summary',
                    ],
                ],
                'required' => ['sentiment', 'score', 'category', 'clean_summary'],
                'additionalProperties' => false,
            ],
        ];

        $response = Http::withToken((string) config('services.openai.key'))
            ->timeout(15)
            ->post('https://api.openai.com/v1/chat/completions', [
                'model' => 'gpt-4o-mini',
                'messages' => [
                    ['role' => 'system', 'content' => 'Analyze the customer feedback text. Output only valid JSON following schema.'],
                    ['role' => 'user', 'content' => $feedbackText],
                ],
                'response_format' => [
                    'type' => 'json_schema',
                    'json_schema' => $jsonSchema,
                ],
            ]);

        if (!$response->successful()) {
            throw new RuntimeException('AI service request failed.');
        }

        $rawJson = (string) $response->json('choices.0.message.content');
        $decoded = json_decode($rawJson, true, 512, JSON_THROW_ON_ERROR);

        if (!is_array($decoded)) {
            throw new RuntimeException('Model response is not a valid JSON structure.');
        }

        // Validate the structure with Laravel Validator
        $validated = Validator::make($decoded, [
            'sentiment' => ['required', 'string', 'in:positive,neutral,negative'],
            'score' => ['required', 'numeric', 'between:0,1'],
            'category' => ['required', 'string', 'in:billing,technical,sales,general'],
            'clean_summary' => ['required', 'string', 'max:500'],
        ])->validate();

        // Strip any residual HTML tags before passing downstream
        $validated['clean_summary'] = strip_tags($validated['clean_summary']);

        return $validated;
    }
}
```

## Blade Template Best Practice

When rendering AI-generated text in Laravel Blade views, **never** use unescaped `{!! !!}` tags:

```blade
{{-- [INSECURE]: Vulnerable to second-order XSS from hallucinated or injected HTML --}}
<div>{!! $aiSummary !!}</div>

{{-- [SECURE]: Automatically escaped by Blade using htmlspecialchars() --}}
<div>{{ $aiSummary }}</div>

{{-- [SECURE]: If Markdown is required, use Laravel's Str::markdown with safe options --}}
<div>
    {!! \Illuminate\Support\Str::markdown($aiSummary, [
        'html_input' => 'strip',
        'allow_unsafe_links' => false,
    ]) !!}
</div>
```

## Laravel-Specific Notes

- **Prepared Statements**: Always pass model outputs as bound parameters in Eloquent (`User::where('summary', $aiSummary)->...`) or PDO statements. Zero concatenation.
- **Markdown Security**: If rendering model-generated Markdown, configure CommonMark or `Str::markdown()` with `'html_input' => 'strip'` and `'allow_unsafe_links' => false` to block `javascript:` links and inline HTML.
- **Process Isolation**: Never pass model outputs directly to `Process::run()`, `exec()`, or `shell_exec()`. Use strictly allowlisted identifiers.

## Checklist

- [ ] AI model outputs are treated as untrusted user data.
- [ ] Structured Outputs (JSON Schema) are used instead of free-form strings where programmatic downstream parsing is needed.
- [ ] Downstream SQL queries use parameterized PDO bindings, never string concatenation.
- [ ] Blade views use standard `{{ $output }}` escaping or sanitized `Str::markdown(..., ['html_input' => 'strip'])`.
- [ ] No model outputs are passed to shell execution functions.

## Further Reading

- [OWASP Top 10 for LLM Applications (LLM05: Improper Output Handling)](https://genai.owasp.org/llm-top-10/)
- [OpenAI Structured Outputs & JSON Schema Documentation](https://platform.openai.com/docs/guides/structured-outputs)
- [Laravel Blade Templating & HTML Escaping](https://laravel.com/docs/13.x/blade)
