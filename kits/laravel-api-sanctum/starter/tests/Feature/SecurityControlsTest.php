<?php

namespace Tests\Feature;

use App\Models\Project;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\RateLimiter;
use Laravel\Sanctum\Sanctum;
use Tests\TestCase;

/**
 * Each test here backs a control declared in security/checks.json.
 * The control id is named so a reader can trace claim -> proof.
 */
class SecurityControlsTest extends TestCase
{
    use RefreshDatabase;

    // --- SEC-02: BOLA / IDOR model policy authorization --------------------

    public function test_sec02_user_cannot_update_another_users_project(): void
    {
        $owner = User::factory()->create();
        $attacker = User::factory()->create();
        $project = Project::factory()->create(['user_id' => $owner->id]);

        Sanctum::actingAs($attacker, ['projects:read', 'projects:write']);

        $this->putJson("/api/v1/projects/{$project->id}", [
            'title' => 'Hijacked',
            'status' => 'active',
            'priority' => 1,
        ])->assertStatus(403);

        $this->assertNotSame('Hijacked', $project->fresh()->title);
    }

    public function test_sec02_user_cannot_delete_another_users_project(): void
    {
        $owner = User::factory()->create();
        $attacker = User::factory()->create();
        $project = Project::factory()->create(['user_id' => $owner->id]);

        Sanctum::actingAs($attacker, ['projects:read', 'projects:write']);

        $this->deleteJson("/api/v1/projects/{$project->id}")->assertStatus(403);
        $this->assertDatabaseHas('projects', ['id' => $project->id]);
    }

    // --- SEC-03: tenant isolation in query lists ---------------------------

    public function test_sec03_list_never_leaks_another_tenants_rows(): void
    {
        $owner = User::factory()->create();
        $other = User::factory()->create();
        Project::factory()->count(2)->create(['user_id' => $owner->id]);
        Project::factory()->count(3)->create(['user_id' => $other->id]);

        Sanctum::actingAs($owner, ['projects:read']);

        $response = $this->getJson('/api/v1/projects')->assertOk();
        $this->assertCount(2, $response->json('data'));
    }

    // --- SEC-04: granular token ability scopes -----------------------------

    public function test_sec04_token_without_read_ability_is_refused(): void
    {
        $user = User::factory()->create();
        Sanctum::actingAs($user, ['projects:write']);

        $this->getJson('/api/v1/projects')->assertStatus(403);
    }

    public function test_sec04_token_with_correct_ability_is_allowed(): void
    {
        $user = User::factory()->create();
        Sanctum::actingAs($user, ['projects:read']);

        $this->getJson('/api/v1/projects')->assertOk();
    }

    // --- SEC-06: rate limiting on the credential endpoint ------------------

    public function test_sec06_login_endpoint_throttles_after_ten_attempts(): void
    {
        RateLimiter::clear('');
        $user = User::factory()->create();

        $statuses = [];
        for ($i = 0; $i < 12; $i++) {
            $statuses[] = $this->postJson('/api/v1/auth/token', [
                'email' => $user->email,
                'password' => 'wrong-password',
                'device_name' => 'test',
            ])->getStatusCode();
        }

        $this->assertContains(429, $statuses, 'login endpoint never returned 429; throttle is not enforced');
    }

    // --- SEC-07: strict resource serialization -----------------------------

    public function test_sec07_password_hash_is_never_serialized(): void
    {
        $user = User::factory()->create();
        Sanctum::actingAs($user, ['projects:read', 'projects:write']);

        $body = $this->getJson('/api/v1/auth/me')->assertOk()->getContent();

        $this->assertStringNotContainsString('password', $body);
        $this->assertStringNotContainsString('remember_token', $body);
    }

    // --- SEC-08: Spatie allowed-filter whitelist ---------------------------

    public function test_sec08_filter_outside_the_whitelist_is_rejected(): void
    {
        $user = User::factory()->create();
        Sanctum::actingAs($user, ['projects:read']);

        // user_id is deliberately not an allowed filter; permitting it would
        // let a caller pivot the tenant scope.
        $this->getJson('/api/v1/projects?filter[user_id]=1')->assertStatus(400);
    }

    public function test_sec08_whitelisted_filter_still_works(): void
    {
        $user = User::factory()->create();
        Project::factory()->create(['user_id' => $user->id, 'status' => 'active']);
        Project::factory()->create(['user_id' => $user->id, 'status' => 'draft']);

        Sanctum::actingAs($user, ['projects:read']);

        $response = $this->getJson('/api/v1/projects?filter[status]=active')->assertOk();
        $this->assertCount(1, $response->json('data'));
    }

    // --- Mass assignment: payload cannot reassign ownership ----------------

    public function test_mass_assignment_cannot_set_user_id_from_payload(): void
    {
        $user = User::factory()->create();
        $victim = User::factory()->create();

        Sanctum::actingAs($user, ['projects:write']);

        $this->postJson('/api/v1/projects', [
            'title' => 'Ownership test',
            'status' => 'draft',
            'priority' => 3,
            'user_id' => $victim->id,
        ])->assertStatus(201);

        $this->assertDatabaseHas('projects', [
            'title' => 'Ownership test',
            'user_id' => $user->id,
        ]);
        $this->assertDatabaseMissing('projects', [
            'title' => 'Ownership test',
            'user_id' => $victim->id,
        ]);
    }

    // --- SEC-12: form request validation -----------------------------------

    public function test_sec12_invalid_status_is_rejected(): void
    {
        $user = User::factory()->create();
        Sanctum::actingAs($user, ['projects:write']);

        $this->postJson('/api/v1/projects', [
            'title' => 'Bad status',
            'status' => 'not-a-real-status',
            'priority' => 3,
        ])->assertStatus(422)->assertJsonValidationErrors('status');
    }

    public function test_sec12_priority_outside_range_is_rejected(): void
    {
        $user = User::factory()->create();
        Sanctum::actingAs($user, ['projects:write']);

        $this->postJson('/api/v1/projects', [
            'title' => 'Bad priority',
            'status' => 'draft',
            'priority' => 99,
        ])->assertStatus(422)->assertJsonValidationErrors('priority');
    }

    // --- SEC-13: stateless API, no CSRF token required ---------------------

    public function test_sec13_write_succeeds_with_bearer_token_and_no_csrf_token(): void
    {
        $user = User::factory()->create();
        Sanctum::actingAs($user, ['projects:write']);

        $this->postJson('/api/v1/projects', [
            'title' => 'Stateless write',
            'status' => 'draft',
            'priority' => 2,
        ])->assertStatus(201);
    }

    // --- SEC-10: no committed secrets --------------------------------------

    public function test_sec10_env_example_ships_no_real_secret(): void
    {
        $path = dirname(__DIR__, 2) . '/.env.example';
        $contents = file_get_contents($path);

        $this->assertStringStartsNotWith("\u{FEFF}", $contents, '.env.example starts with a UTF-8 BOM');

        foreach (explode("\n", $contents) as $line) {
            if (str_starts_with(trim($line), 'APP_KEY=')) {
                $value = trim(substr(trim($line), strlen('APP_KEY=')));
                $this->assertSame('', $value, 'APP_KEY must ship empty, never with a real key');
            }
        }
    }

    // --- SEC-05: token expiration is configured ----------------------------

    public function test_sec05_token_expiration_is_configured(): void
    {
        $this->assertNotNull(
            config('sanctum.expiration'),
            'sanctum.expiration is null; tokens would never expire'
        );
    }
}
