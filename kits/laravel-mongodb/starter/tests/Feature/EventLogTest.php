<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Models\EventLog;
use Illuminate\Auth\GenericUser;
use Tests\TestCase;

/**
 * Requires a live MongoDB (see phpunit.xml: MONGODB_URI). These tests cannot
 * run against SQLite.
 */
class EventLogTest extends TestCase
{
    protected function setUp(): void
    {
        parent::setUp();
        EventLog::query()->delete();
    }

    private function user(string $id = '507f1f77bcf86cd799439011'): GenericUser
    {
        return new GenericUser(['id' => $id, 'name' => 'Tester', 'email' => "{$id}@example.test"]);
    }

    public function test_healthz_endpoint_returns_ok(): void
    {
        $this->get('/healthz')
            ->assertStatus(200)
            ->assertJson(['status' => 'ok', 'driver' => 'mongodb']);
    }

    public function test_can_query_events_and_aggregation_pipeline(): void
    {
        $user = $this->user();
        EventLog::create([
            'user_id' => (string) $user->id,
            'category' => 'security',
            'action' => 'blocked_nosql_injection',
            'severity' => 'high',
            'latency_ms' => 5,
        ]);

        $this->actingAs($user)->getJson('/events')
            ->assertStatus(200)
            ->assertJsonStructure(['status', 'total_events', 'category_stats', 'recent_events'])
            ->assertJsonPath('total_events', 1);
    }

    public function test_rejects_dollar_sign_operator_injection(): void
    {
        $this->actingAs($this->user())->postJson('/events', [
            'category' => 'audit',
            'action' => 'malicious_test',
            'severity' => 'critical',
            'metadata' => ['$where' => 'function() { return true; }'],
        ])->assertStatus(422);

        $this->assertSame(0, EventLog::count());
    }

    public function test_stores_a_valid_event_for_the_caller(): void
    {
        $user = $this->user();

        $this->actingAs($user)->postJson('/events', [
            'category' => 'audit',
            'action' => 'created',
            'severity' => 'low',
            'metadata' => ['ip' => '127.0.0.1'],
        ])->assertStatus(201);

        $this->assertSame((string) $user->id, EventLog::first()->user_id);
    }
}
