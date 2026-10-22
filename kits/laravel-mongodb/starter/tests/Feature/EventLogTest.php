<?php

namespace Tests\Feature;

use App\Models\EventLog;
use Tests\TestCase;

class EventLogTest extends TestCase
{
    public function test_healthz_endpoint_returns_ok(): void
    {
        $response = $this->get('/healthz');
        $response->assertStatus(200);
        $response->assertJson([
            'status' => 'ok',
            'driver' => 'mongodb',
        ]);
    }

    public function test_can_query_events_and_aggregation_pipeline(): void
    {
        EventLog::create([
            'user_id' => 'test-user',
            'category' => 'security',
            'action' => 'blocked_nosql_injection',
            'severity' => 'high',
            'latency_ms' => 5,
        ]);

        $response = $this->get('/events');
        $response->assertStatus(200);
        $response->assertJsonStructure([
            'status',
            'total_events',
            'category_stats',
            'recent_events'
        ]);
    }

    public function test_rejects_dollar_sign_operator_injection(): void
    {
        $response = $this->postJson('/events', [
            'category' => 'audit',
            'action' => 'malicious_test',
            'severity' => 'critical',
            'metadata' => [
                '$where' => 'function() { return true; }'
            ]
        ]);

        $response->assertStatus(422);
    }
}
