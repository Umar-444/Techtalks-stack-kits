<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Models\Document;
use App\Services\AiService;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class DocumentSeeder extends Seeder
{
    public function run(): void
    {
        $ai = new AiService();

        $docs = [
            ['title' => 'Security Guardrails', 'content' => 'Zero-trust architecture mandates strict input delimiters and token budgeting.', 'tenant_id' => 1],
            ['title' => 'Vector Indexing', 'content' => 'PostgreSQL pgvector HNSW indexes provide sub-linear search latency for cosine distance.', 'tenant_id' => 1],
            ['title' => 'Tenant Separation', 'content' => 'Documents are isolated by tenant_id column at the database query boundary.', 'tenant_id' => 2],
        ];

        foreach ($docs as $d) {
            $embedding = $ai->generateEmbedding($d['content']);
            $embeddingJson = '[' . implode(',', $embedding) . ']';

            DB::statement(
                "INSERT INTO documents (title, content, tenant_id, embedding, created_at, updated_at) VALUES (?, ?, ?, ?::vector, NOW(), NOW())",
                [$d['title'], $d['content'], $d['tenant_id'], $embeddingJson]
            );
        }
    }
}
