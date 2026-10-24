<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Models\EventLog;
use App\Models\User;
use Illuminate\Auth\GenericUser;
use Illuminate\Support\Facades\Hash;
use MongoDB\Laravel\Eloquent\DocumentModel;
use MongoDB\Laravel\Eloquent\Model as MongoModel;
use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

/**
 * Controls declared in security/checks.json that this kit's code implements.
 *
 * Requires a live MongoDB (see phpunit.xml) and the ext-mongodb PHP extension.
 * MongoDB cannot be emulated by SQLite, so these tests have NOT been run in
 * the environment where this suite was written (no mongod, no ext-mongodb).
 *
 * NOT covered, because the kit ships no implementation: NOSQL-02 (ObjectId
 * validation, there is no by-id route), NOSQL-03 (TLS is deployment config),
 * NOSQL-04 (collection JSON-schema validation), NOSQL-05 (index guard) and
 * AUTH-03. CI-01/02 are pipeline gates.
 */
class SecurityControlsTest extends TestCase
{
    protected function setUp(): void
    {
        parent::setUp();
        EventLog::query()->delete();
    }

    /** A plain authenticated identity: no database or driver needed to build it. */
    private function user(string $id): GenericUser
    {
        return new GenericUser(['id' => $id, 'name' => 'Tester', 'email' => "{$id}@example.test"]);
    }

    private function mongoUser(string $id): User
    {
        return (new User)->forceFill(['_id' => $id, 'name' => 'Tester', 'email' => "{$id}@example.test"]);
    }

    private function payload(array $overrides = []): array
    {
        return array_merge(['category' => 'audit', 'action' => 'test', 'severity' => 'low'], $overrides);
    }

    // Authentication gate
    public function test_unauthenticated_requests_are_refused(): void
    {
        $this->getJson('/events')->assertStatus(401);
        $this->postJson('/events', $this->payload())->assertStatus(401);
        $this->assertSame(0, EventLog::count());
    }

    // NOSQL-01
    #[DataProvider('operatorPayloads')]
    public function test_operator_keys_are_rejected_at_any_depth(array $metadata): void
    {
        $this->actingAs($this->user('507f1f77bcf86cd799439011'))
            ->postJson('/events', $this->payload(['metadata' => $metadata]))
            ->assertStatus(422);

        $this->assertSame(0, EventLog::count());
    }

    public static function operatorPayloads(): array
    {
        return [
            'top level where' => [['$where' => 'sleep(1000)']],
            'top level ne' => [['$ne' => null]],
            'nested operator' => [['filter' => ['$gt' => '']]],
            'deeply nested' => [['a' => ['b' => ['c' => ['$regex' => '.*']]]]],
            'dotted path key' => [['profile.role' => 'admin']],
        ];
    }

    public function test_plain_metadata_is_accepted(): void
    {
        $this->actingAs($this->user('507f1f77bcf86cd799439011'))
            ->postJson('/events', $this->payload(['metadata' => ['ip' => '10.0.0.1', 'nested' => ['ok' => true]]]))
            ->assertStatus(201);
    }

    // DATA-01
    public function test_input_is_validated(): void
    {
        $user = $this->user('507f1f77bcf86cd799439011');

        foreach ([
            ['severity' => 'catastrophic'],
            ['category' => str_repeat('x', 51)],
            ['latency_ms' => -1],
            ['latency_ms' => 'fast'],
            ['metadata' => 'not-an-array'],
        ] as $bad) {
            $this->actingAs($user)->postJson('/events', $this->payload($bad))->assertStatus(422);
        }

        $this->assertSame(0, EventLog::count());
    }

    public function test_client_cannot_choose_the_owner(): void
    {
        $user = $this->user('507f1f77bcf86cd799439011');

        $this->actingAs($user)
            ->postJson('/events', $this->payload(['user_id' => 'someone-else']))
            ->assertStatus(201);

        $this->assertSame('507f1f77bcf86cd799439011', EventLog::first()->user_id);
    }

    // AUTH-02
    public function test_users_only_see_their_own_events(): void
    {
        EventLog::create($this->payload(['user_id' => 'owner-a', 'category' => 'mine', 'latency_ms' => 1]));
        EventLog::create($this->payload(['user_id' => 'owner-b', 'category' => 'theirs', 'latency_ms' => 2]));

        $response = $this->actingAs($this->user('owner-a'))->getJson('/events')->assertOk();

        $this->assertSame(1, $response->json('total_events'));
        $this->assertSame(['mine'], array_column($response->json('recent_events'), 'category'));
        $this->assertSame(['mine'], array_column($response->json('category_stats'), '_id'));
    }

    public function test_policy_allows_only_the_owner(): void
    {
        $event = (new EventLog)->forceFill(['user_id' => 'owner-a']);

        foreach (['view', 'update', 'delete'] as $ability) {
            $this->assertTrue($this->mongoUser('owner-a')->can($ability, $event));
            $this->assertFalse($this->mongoUser('owner-b')->can($ability, $event));
        }
    }

    // Model hygiene
    public function test_models_extend_the_mongodb_base_model_and_whitelist_fields(): void
    {
        foreach ([EventLog::class, User::class] as $class) {
            $this->assertTrue(
                is_subclass_of($class, MongoModel::class) || in_array(DocumentModel::class, class_uses_recursive($class), true),
                "{$class} must be a MongoDB document model"
            );
            $this->assertNotEmpty((new $class)->getFillable());
        }
    }

    public function test_user_cannot_mass_assign_privileges(): void
    {
        $user = (new User)->fill(['name' => 'x', 'is_admin' => true, 'role' => 'admin']);

        $this->assertNull($user->is_admin);
        $this->assertNull($user->role);
    }

    // AUTH-01
    public function test_password_is_hashed_with_a_strong_driver(): void
    {
        $this->assertSame('argon2id', config('hashing.driver'));
        $this->assertGreaterThanOrEqual(65536, config('hashing.argon.memory'));
        $this->assertStringStartsWith('$argon2id$', Hash::make('secret-value'));
    }

    // DATA-02
    public function test_connection_pool_and_timeouts_are_capped(): void
    {
        $options = config('database.connections.mongodb.options');

        $this->assertLessThanOrEqual(100, $options['maxPoolSize']);
        $this->assertGreaterThan(0, $options['serverSelectionTimeoutMS']);
        $this->assertLessThanOrEqual(10000, $options['serverSelectionTimeoutMS']);
        $this->assertLessThanOrEqual(60000, $options['socketTimeoutMS']);
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
