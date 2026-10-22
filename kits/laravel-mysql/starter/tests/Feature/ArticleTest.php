<?php

namespace Tests\Feature;

use App\Models\Article;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ArticleTest extends TestCase
{
    use RefreshDatabase;

    public function test_healthz_endpoint(): void
    {
        $response = $this->getJson('/healthz');
        $response->assertStatus(200)
                 ->assertJson([
                     'status' => 'ok',
                     'app' => 'laravel-mysql',
                 ]);
    }

    public function test_lists_articles(): void
    {
        $user = User::factory()->create();
        Article::factory()->create(['user_id' => $user->id, 'status' => 'published']);

        $response = $this->getJson('/api/articles');
        $response->assertStatus(200);
    }
}
