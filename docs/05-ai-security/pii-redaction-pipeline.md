# PII Redaction Pipeline in Laravel

> Last reviewed: 2026-10. Applies to: PHP 8.4+, Laravel 11.x – 13.x.

## Quick Answer

A Personally Identifiable Information (PII) redaction pipeline automatically detects, masks, or pseudonymizes sensitive data (emails, phone numbers, credit cards, national IDs) before user text is transmitted to external LLM APIs. In Laravel, this pipeline operates as a pre-processing middleware or service that strips confidential data, replaces it with cryptographic placeholders, and optionally restores the original values when presenting answers back to the authenticated user.

## Threat Model

- **Attacker Profile**: Adversaries listening on third-party APIs, untrusted LLM providers logging prompt histories, or employees with data inspection access.
- **Attack Vectors**:
  - **Third-Party Model Training Leaks**: Users pasting credit cards, social security numbers, or patient medical numbers into support chats that get logged on third-party AI provider servers.
  - **Regulatory Non-Compliance**: Transmitting citizen identifiers across geographic borders in violation of GDPR, HIPAA, or the Saudi Personal Data Protection Law (PDPL).
- **Impact & Cost**: Regulatory fines, customer trust loss, identity theft, and enterprise breach penalties.

## Vulnerable Example

```php
<?php

declare(strict_types=1);

namespace App\Services\Ai;

use Illuminate\Support\Facades\Http;

class VulnerableSupportBot
{
    /**
     * [INSECURE]: Transmitting raw, unredacted customer data directly to an external API.
     */
    public function analyzeTicket(string $ticketText): string
    {
        // Vulnerable: raw text containing SSNs, phone numbers, or credit cards sent over wire
        $response = Http::withToken((string) config('services.openai.key'))
            ->post('https://api.openai.com/v1/chat/completions', [
                'model' => 'gpt-4o-mini',
                'messages' => [
                    ['role' => 'user', 'content' => "Categorize this support ticket:\n" . $ticketText],
                ],
            ]);

        return (string) $response->json('choices.0.message.content');
    }
}
```

## Secure Implementation

```php
<?php

declare(strict_types=1);

namespace App\Services\Ai\Support;

final class PiiRedactor
{
    /** @var array<string, string> Map of regex patterns to replacement tokens */
    private const array PATTERNS = [
        // Credit Card Numbers (Major card formats)
        '/\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b/'
            => '[REDACTED_CREDIT_CARD]',

        // Email Addresses
        '/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/'
            => '[REDACTED_EMAIL]',

        // International and Local Phone Numbers (E.164 and common formats)
        '/(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}/'
            => '[REDACTED_PHONE]',

        // Saudi National ID / Iqama (10 digits starting with 1 or 2)
        '/\b[12]\d{9}\b/'
            => '[REDACTED_NATIONAL_ID]',

        // US Social Security Numbers
        '/\b\d{3}-\d{2}-\d{4}\b/'
            => '[REDACTED_SSN]',
    ];

    /**
     * [SECURE]: Scans input string and replaces sensitive entities with sanitized tokens.
     */
    public function redact(string $text): string
    {
        $sanitized = $text;

        foreach (self::PATTERNS as $pattern => $replacement) {
            $sanitized = (string) preg_replace($pattern, $replacement, $sanitized);
        }

        return $sanitized;
    }

    /**
     * Checks whether a string contains any detectable PII entities.
     */
    public function containsPii(string $text): bool
    {
        foreach (array_keys(self::PATTERNS) as $pattern) {
            if (preg_match($pattern, $text) === 1) {
                return true;
            }
        }

        return false;
    }
}
```

## Integrating with Laravel AI Service

```php
<?php

declare(strict_types=1);

namespace App\Services\Ai;

use App\Services\Ai\Support\PiiRedactor;
use Illuminate\Support\Facades\Http;
use RuntimeException;

final class SecureTicketAnalysisService
{
    public function __construct(
        private readonly PiiRedactor $redactor
    ) {}

    public function analyzeTicket(string $rawTicket): string
    {
        // Redact all sensitive identifiers before making outbound network requests
        $sanitizedTicket = $this->redactor->redact($rawTicket);

        $response = Http::withToken((string) config('services.openai.key'))
            ->timeout(15)
            ->post('https://api.openai.com/v1/chat/completions', [
                'model' => 'gpt-4o-mini',
                'messages' => [
                    ['role' => 'system', 'content' => 'Categorize the support inquiry. Sensitive details are replaced with tokens.'],
                    ['role' => 'user', 'content' => $sanitizedTicket],
                ],
            ]);

        if (!$response->successful()) {
            throw new RuntimeException('Failed to analyze ticket with AI provider.');
        }

        return (string) $response->json('choices.0.message.content');
    }
}
```

## Laravel-Specific Notes

- **Model Observers**: If your application stores chat logs or prompt histories in the database, attach an Eloquent `saving` observer to automatically redact sensitive fields before saving to disk.
- **Saudi PDPL Compliance**: Under the Saudi Personal Data Protection Law (PDPL), transferring national citizen data to foreign AI servers without explicit consent or adequacy agreements is restricted. Pre-scrubbing national IDs and contact information ensures compliance.
- **Zero-Data Retention Agreements**: In addition to local redaction, configure the "Zero Data Retention" (ZDR) policy in your enterprise OpenAI/Anthropic/AWS Bedrock agreement.

## Checklist

- [ ] PII redaction runs prior to every external LLM API request.
- [ ] Patterns cover emails, phone numbers, credit cards, and regional identifiers (SSN, Saudi National ID).
- [ ] Unit tests verify regex matching and substitution across known edge cases.
- [ ] Chat conversation logs stored in database are scrubbed of sensitive credentials.
- [ ] Third-party model training opting-out is configured in the AI provider dashboard.

## Further Reading

- [OWASP Top 10 for LLM Applications (LLM02: Sensitive Information Disclosure)](https://genai.owasp.org/llm-top-10/)
- [Saudi Data & AI Authority (SDAIA) - Personal Data Protection Law (PDPL)](https://sdaia.gov.sa/)
- [NIST Privacy Framework (NIST CSWP 21)](https://www.nist.gov/privacy-framework)
