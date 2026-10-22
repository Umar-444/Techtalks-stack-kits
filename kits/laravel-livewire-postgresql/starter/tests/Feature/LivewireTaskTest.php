<?php

namespace Tests\Feature;

use App\Livewire\TaskManager;
use App\Models\User;
use App\Models\Task;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Livewire\Livewire;
use Tests\TestCase;

class LivewireTaskTest extends TestCase
{
    use RefreshDatabase;

    public function test_healthz_endpoint_returns_ok(): void
    {
        $response = $this->get('/healthz');
        $response->assertStatus(200);
        $response->assertJson([
            'status' => 'ok',
            'app' => 'laravel-livewire-postgresql'
        ]);
    }

    public function test_can_create_task_via_livewire(): void
    {
        $user = User::factory()->create();

        Livewire::actingAs($user)
            ->test(TaskManager::class)
            ->set('title', 'Deploy Volt Component')
            ->set('priority', 'high')
            ->call('save')
            ->assertHasNoErrors()
            ->assertSee('Deploy Volt Component');

        $this->assertDatabaseHas('tasks', [
            'title' => 'Deploy Volt Component',
            'user_id' => $user->id,
        ]);
    }
}
