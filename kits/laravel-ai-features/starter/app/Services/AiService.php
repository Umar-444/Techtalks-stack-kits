<?php

declare(strict_types=1);

namespace App\Services;

use InvalidArgumentException;
use RuntimeException;

class AiService
{
    private array $jailbreakPatterns = [
        '/ignore\s+(all\s+)?previous\s+instructions/i',
        '/you\s+are\s+now\s+dan/i',
        '/reveal\s+(the\s+)?system\s+prompt/i',
        '/bypass\s+guardrails/i',
    ];

    public function screenPrompt(string $prompt): string
    {
        foreach ($this->jailbreakPatterns as $pattern) {
            if (preg_match($pattern, $prompt)) {
                throw new InvalidArgumentException("Potential prompt injection pattern detected.");
            }
        }

        // Return encapsulated sanitized prompt
        return "<user_query>" . htmlspecialchars($prompt, ENT_QUOTES, 'UTF-8') . "</user_query>";
    }

    public function structuredCompletion(string $prompt, array $schema): array
    {
        $sanitized = $this->screenPrompt($prompt);

        // Deterministic mock synthesis for test/production-safe verification
        return [
            'summary' => "Synthesized answer for: " . substr($prompt, 0, 40),
            'confidence' => 0.98,
            'citations' => ['doc-001', 'doc-002'],
        ];
    }

    public function generateEmbedding(string $text): array
    {
        // 1536-dimensional mock embedding for deterministic cosine tests
        $hash = md5($text);
        $vector = [];
        for ($i = 0; $i < 1536; $i++) {
            $vector[] = round(sin($i + hexdec(substr($hash, $i % 30, 2))), 4);
        }
        return $vector;
    }
}
