# RAG Tenant Isolation in Laravel

> Last reviewed: 2026-10. Applies to: PHP 8.4+, Laravel 11.x – 13.x.

## Quick Answer

Retrieval-Augmented Generation (RAG) tenant isolation guarantees that an AI model only incorporates documents owned by the currently authenticated tenant. Tenant boundaries must be enforced at the retrieval layer (via database and vector search metadata filters), never at generation time via system prompt instructions. Instructing a model to "only discuss user A's data" after feeding it user B's documents is vulnerable to prompt injection and context leakage.

## Threat Model

- **Attacker Profile**: Authenticated multi-tenant SaaS users attempting horizontal privilege escalation.
- **Attack Vectors**:
  - **Prompt Leaking via Semantic Similarity**: User asks: `What was the revenue in the Q3 confidential report?`. If vector retrieval searches across all company embeddings without tenant IDs, competitor or other tenant chunks enter the prompt.
  - **Indirect Cross-Tenant Injection**: Injecting adversarial instructions into user A's uploaded documents that trigger when user B searches for common terms.
- **Impact & Cost**: Catastrophic data breach, violation of privacy regulations (GDPR, Saudi PDPL), and contractual compliance failure.

## Vulnerable Example

```php
<?php

declare(strict_types=1);

namespace App\Services\Ai;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

class VulnerableRagService
{
    /**
     * [INSECURE]: Vector search retrieves documents without filtering by tenant_id.
     * The developer relies on the prompt to "ignore other users".
     */
    public function queryRag(string $userQuery, int $tenantId): string
    {
        // Vulnerable: Global embedding similarity search across the entire database!
        $embedding = $this->getEmbedding($userQuery);

        $documents = DB::select("
            SELECT content, tenant_id
            FROM document_chunks
            ORDER BY embedding <=> ?::vector
            LIMIT 5
        ", [json_encode($embedding)]);

        // Relying on prompt to filter tenant data is completely bypassable
        $context = collect($documents)->pluck('content')->implode("\n---\n");
        $systemPrompt = "You are an assistant for tenant #{$tenantId}. Only answer questions using data belonging to this tenant.";

        return $this->askLlm($systemPrompt, $userQuery, $context);
    }
}
```

## Secure Implementation

```php
<?php

declare(strict_types=1);

namespace App\Services\Ai;

use App\Models\DocumentChunk;
use App\Models\User;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Http;
use RuntimeException;

final class SecureRagTenantIsolationService
{
    /**
     * [SECURE]: Hard tenant isolation enforced strictly at the query/vector retrieval layer.
     */
    public function queryTenantRag(User $user, string $userQuery): string
    {
        $tenantId = $user->tenant_id;
        if ($tenantId === null) {
            throw new RuntimeException('Authenticated user has no associated tenant ID.');
        }

        $queryEmbedding = $this->generateEmbedding($userQuery);

        // Enforce hard tenant scoping directly in PostgreSQL pgvector / MySQL query
        $relevantChunks = DocumentChunk::query()
            ->where('tenant_id', $tenantId) // HARD ISOLATION FILTER
            ->whereHas('document', function (Builder $query) use ($user) {
                // Secondary ACL: Verify user has permission to read this document
                $query->where('visibility', 'public')
                    ->orWhere('owner_id', $user->id);
            })
            ->orderByRaw('embedding <=> ?::vector', [json_encode($queryEmbedding)])
            ->limit(4)
            ->get();

        if ($relevantChunks->isEmpty()) {
            return 'No relevant tenant documentation was found to answer your inquiry.';
        }

        $contextBlocks = $relevantChunks
            ->map(fn (DocumentChunk $chunk) => "<doc id=\"{$chunk->id}\">\n" . htmlspecialchars($chunk->content, ENT_QUOTES, 'UTF-8') . "\n</doc>")
            ->implode("\n");

        return $this->generateGroundedResponse($contextBlocks, $userQuery);
    }

    private function generateEmbedding(string $text): array
    {
        $response = Http::withToken((string) config('services.openai.key'))
            ->post('https://api.openai.com/v1/embeddings', [
                'model' => 'text-embedding-3-small',
                'input' => $text,
            ]);

        return (array) $response->json('data.0.embedding');
    }

    private function generateGroundedResponse(string $sanitizedContext, string $question): string
    {
        $systemPrompt = <<<SYS
You are an enterprise AI assistant.
Answer the user question using ONLY the provided verified document chunks.
If the answer cannot be found directly in the documents, state that clearly.
SYS;

        $userMessage = <<<USR
<verified_tenant_documents>
{$sanitizedContext}
</verified_tenant_documents>

User Question: {$question}
USR;

        $response = Http::withToken((string) config('services.openai.key'))
            ->post('https://api.openai.com/v1/chat/completions', [
                'model' => 'gpt-4o-mini',
                'temperature' => 0.1,
                'messages' => [
                    ['role' => 'system', 'content' => $systemPrompt],
                    ['role' => 'user', 'content' => $userMessage],
                ],
            ]);

        return (string) $response->json('choices.0.message.content');
    }
}
```

## Laravel-Specific Notes

- **Global Scopes**: Implement a `TenantScope` on your `DocumentChunk` and `Document` Eloquent models to automatically append `WHERE tenant_id = ?` to every query by default.
- **Vector Database Metadata**: If using Pinecone, Qdrant, or Weaviate, always pass `filter: { "tenant_id": { "$eq": $tenantId } }` inside the vector search payload.
- **Tenant Context Verification**: In your controller or middleware, ensure `tenant_id` is derived from authenticated session state (`auth()->user()->tenant_id`), never from request body parameters like `$request->input('tenant_id')`.

## Checklist

- [ ] Multi-tenant vector searches include hard `tenant_id` filters in the retrieval query.
- [ ] Retrieval never relies on the LLM to filter or ignore cross-tenant chunks.
- [ ] Document chunks inherit parent document authorization policies (ACL).
- [ ] Tenant identifier is sourced exclusively from authenticated user session/token.
- [ ] Retrieved chunk content is delimited and escaped before insertion into the context prompt.

## Further Reading

- [OWASP Top 10 for LLM Applications (LLM02: Sensitive Information Disclosure)](https://genai.owasp.org/llm-top-10/)
- [PostgreSQL pgvector Extension Security & Query Scoping](https://github.com/pgvector/pgvector)
- [Laravel Multi-Tenancy Architecture Patterns](https://laravel.com/docs/13.x/eloquent)
