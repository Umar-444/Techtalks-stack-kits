<?php

namespace Tests\Feature;

use App\Models\Project;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Sanctum\Sanctum;
use Tests\TestCase;

class ProjectApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_unauthenticated_request_returns_401(): void
    {
        $response = $this->getJson('/api/v1/projects');
        $response->assertStatus(401);
    }

    public function test_user_can_list_only_own_projects(): void
    {
        $user1 = User::factory()->create();
        $user2 = User::factory()->create();

        Project::factory()->create(['user_id' => $user1->id, 'title' => 'User1 Project']);
        Project::factory()->create(['user_id' => $user2->id, 'title' => 'User2 Project']);

        Sanctum::actingAs($user1, ['projects:read']);

        $response = $this->getJson('/api/v1/projects');
        $response->assertStatus(200);
        $response->assertJsonCount(1, 'data');
        $response->assertJsonPath('data.0.title', 'User1 Project');
    }

    public function test_user_cannot_access_other_user_project_bola_prevented(): void
    {
        $user1 = User::factory()->create();
        $user2 = User::factory()->create();

        $projectOfUser2 = Project::factory()->create(['user_id' => $user2->id]);

        Sanctum::actingAs($user1, ['projects:read', 'projects:write']);

        // Attempting to read another user's project returns 403 Forbidden
        $response = $this->getJson("/api/v1/projects/{$projectOfUser2->id}");
        $response->assertStatus(403);

        // Attempting to mutate another user's project returns 403 Forbidden
        $updateResponse = $this->putJson("/api/v1/projects/{$projectOfUser2->id}", [
            'title' => 'Malicious Hijack Attempt',
        ]);
        $updateResponse->assertStatus(403);
    }

    public function test_token_missing_write_ability_cannot_create_project(): void
    {
        $user = User::factory()->create();
        Sanctum::actingAs($user, ['projects:read']); // read-only token

        $response = $this->postJson('/api/v1/projects', [
            'title' => 'New Project',
            'status' => 'active',
            'priority' => 3,
        ]);

        $response->assertStatus(403);
    }
}
