<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Livewire\TaskManager;
use App\Models\Task;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Livewire\Mechanisms\HandleComponents\CorruptComponentPayloadException;
use Livewire\Exceptions\PublicPropertyNotFoundException;
use Livewire\Livewire;
use Tests\TestCase;

/**
 * Controls declared in security/checks.json that can be exercised without a
 * PostgreSQL server. Runs on SQLite in-memory.
 *
 * Not covered: AUTH-02 (the kit ships no login component to test), DATA-01
 * (the kit has no query-building code beyond plain Eloquent) and CI-01/02
 * (pipeline gates).
 */
class SecurityControlsTest extends TestCase
{
    use RefreshDatabase;

    // LW-01: a tampered snapshot is rejected by the checksum.
    public function test_tampered_snapshot_is_rejected(): void
    {
        $this->actingAs(User::factory()->create());
        $this->withoutExceptionHandling();

        $snapshot = Livewire::test(TaskManager::class)->snapshot;
        $snapshot['data']['title'] = 'injected-by-client';

        $this->expectException(CorruptComponentPayloadException::class);

        $this->postJson('/livewire/update', [
            'components' => [['snapshot' => json_encode($snapshot), 'updates' => [], 'calls' => []]],
        ]);
    }

    public function test_untampered_snapshot_is_accepted(): void
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        $snapshot = Livewire::test(TaskManager::class)->snapshot;

        $this->postJson('/livewire/update', [
            'components' => [['snapshot' => json_encode($snapshot), 'updates' => [], 'calls' => []]],
        ])->assertOk();
    }

    // LW-02: server-side authorization on every action.
    public function test_user_cannot_toggle_another_users_task(): void
    {
        $owner = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $owner->id]);

        Livewire::actingAs(User::factory()->create())
                ->test(TaskManager::class)
                ->call('toggleComplete', $task->id)
            ->assertForbidden();

        $this->assertFalse($task->fresh()->is_completed);
    }

    public function test_user_cannot_delete_another_users_task(): void
    {
        $task = Task::factory()->create();

        Livewire::actingAs(User::factory()->create())
                ->test(TaskManager::class)
                ->call('deleteTask', $task->id)
            ->assertForbidden();

        $this->assertDatabaseHas('tasks', ['id' => $task->id]);
    }

    public function test_guest_cannot_delete(): void
    {
        $task = Task::factory()->create();

        Livewire::test(TaskManager::class)->call('deleteTask', $task->id)
            ->assertForbidden();

        $this->assertDatabaseHas('tasks', ['id' => $task->id]);
    }

    public function test_owner_can_toggle_and_delete(): void
    {
        $owner = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $owner->id]);

        Livewire::actingAs($owner)->test(TaskManager::class)
            ->call('toggleComplete', $task->id)
            ->call('deleteTask', $task->id);

        $this->assertDatabaseMissing('tasks', ['id' => $task->id]);
    }

    public function test_list_only_shows_the_users_own_tasks(): void
    {
        $me = User::factory()->create();
        Task::factory()->create(['user_id' => $me->id, 'title' => 'Mine only']);
        Task::factory()->create(['title' => 'Someone elses secret']);

        Livewire::actingAs($me)->test(TaskManager::class)
            ->assertSee('Mine only')
            ->assertDontSee('Someone elses secret');
    }

    public function test_guest_sees_no_tasks(): void
    {
        Task::factory()->create(['title' => 'Private task']);

        Livewire::test(TaskManager::class)->assertDontSee('Private task');
    }

    // LW-03: ownership cannot be set from the client; bad values are refused.
    public function test_client_cannot_set_the_owner(): void
    {
        $this->expectException(PublicPropertyNotFoundException::class);

        Livewire::actingAs(User::factory()->create())
            ->test(TaskManager::class)
            ->set('user_id', 'someone-else');
    }

    public function test_priority_is_restricted_to_known_values(): void
    {
        Livewire::actingAs(User::factory()->create())
            ->test(TaskManager::class)
            ->set('title', 'A valid title')
            ->set('priority', 'urgent-drop-table')
            ->call('save')
            ->assertHasErrors(['priority']);

        $this->assertSame(0, Task::count());
    }

    // LW-04: length validation.
    public function test_title_and_description_lengths_are_validated(): void
    {
        Livewire::actingAs(User::factory()->create())
            ->test(TaskManager::class)
            ->set('title', str_repeat('a', 151))
            ->set('description', str_repeat('b', 501))
            ->call('save')
            ->assertHasErrors(['title', 'description']);

        $this->assertSame(0, Task::count());
    }

    // LW-05: rate limiting on mutating actions.
    public function test_mutating_actions_are_rate_limited(): void
    {
        $user = User::factory()->create();
        $component = Livewire::actingAs($user)->test(TaskManager::class);

        for ($i = 0; $i < 30; $i++) {
            $component->set('title', "Task number {$i}")->call('save')->assertHasNoErrors();
        }

        $component->set('title', 'One too many')->call('save')->assertHasErrors(['rate']);
        $this->assertSame(30, Task::count());
    }

    // AUTH-01
    public function test_passwords_use_argon2id(): void
    {
        $this->assertSame('argon2id', config('hashing.driver'));
        $this->assertGreaterThanOrEqual(65536, config('hashing.argon.memory'));
        $this->assertStringStartsWith('$argon2id$', Hash::make('secret-value'));
    }

    // AUTH-03
    public function test_session_cookie_flags_are_hardened(): void
    {
        $this->assertTrue(config('session.secure'));
        $this->assertTrue(config('session.http_only'));
        $this->assertSame('lax', config('session.same_site'));
    }

    // DATA-02
    public function test_primary_keys_are_uuids(): void
    {
        $this->assertTrue(Str::isUuid((string) User::factory()->create()->id));
        $this->assertTrue(Str::isUuid((string) Task::factory()->create()->id));
    }

    // Output escaping
    public function test_task_title_is_escaped(): void
    {
        $me = User::factory()->create();
        Task::factory()->create(['user_id' => $me->id, 'title' => '<script>alert(1)</script>']);

        Livewire::actingAs($me)->test(TaskManager::class)
            ->assertDontSeeHtml('<script>alert(1)</script>');
    }

    // Supporting invariants
    public function test_env_example_ships_no_real_key(): void
    {
        $env = file_get_contents(base_path('.env.example'));

        $this->assertStringNotContainsString("\u{FEFF}", $env);
        $this->assertMatchesRegularExpression('/^APP_KEY=\s*$/m', $env);
    }

    public function test_dockerfile_runs_as_non_root(): void
    {
        $this->assertMatchesRegularExpression('/^USER\s+(?!root\b|0\b)\S+/m', file_get_contents(base_path('Dockerfile')));
    }
}
