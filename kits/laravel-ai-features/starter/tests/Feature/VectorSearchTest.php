<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Services\AiService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class VectorSearchTest extends TestCase
{
    public function test_embedding_generation_matches_dimensions(): void
    {
        $ai = new AiService();
        $vector = $ai->generateEmbedding('Sample document passage');
        $this->assertCount(1536, $vector);
    }
}
