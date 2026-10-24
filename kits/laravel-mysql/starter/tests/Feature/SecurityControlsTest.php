<?php

namespace Tests\Feature;

use App\Models\Article;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;
use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

/**
 * The controls declared in security/checks.json, verified.
 *
 * Tests run on SQLite in-memory, so MySQL-specific settings (SQL-02, SQL-03)
 * are asserted against the shipped connection config rather than a live
 * server. Everything else is exercised against real requests.
 */
class SecurityControlsTest extends TestCase
{
    use RefreshDatabase;

    // --- SQL-01: parameterized queries (A05:2025, CWE-89) -----------------

    public function test_search_term_is_bound_not_interpolated(): void
    {
        $author = User::factory()->create();
        Article::factory()->create([
            'user_id' => $author->id,
            'title' => 'Legitimate article',
            'status' => 'published',
        ]);

        $response = $this->getJson("/api/articles?q=" . urlencode("' OR 1=1 --"));

        $response->assertStatus(200);
        // A quote-breaking payload must match nothing, not everything.
        $this->assertSame(0, $response->json('total'));
    }

    public function test_injection_payload_cannot_drop_the_table(): void
    {
        $author = User::factory()->create();
        Article::factory()->count(2)->create(['user_id' => $author->id]);

        $this->getJson("/api/articles?q=" . urlencode("'; DROP TABLE articles; --"));

        $this->assertTrue(Schema::hasTable('articles'));
        $this->assertSame(2, Article::count());
    }

    public function test_legitimate_search_still_matches(): void
    {
        // Guards against the injection tests passing vacuously because search
        // returns nothing for every input.
        $author = User::factory()->create();
        Article::factory()->create([
            'user_id' => $author->id,
            'title' => 'Distinctive marker phrase',
            'status' => 'published',
        ]);

        $response = $this->getJson('/api/articles?q=Distinctive');

        $response->assertStatus(200);
        $this->assertSame(1, $response->json('total'));
    }

    // --- SQL-02 / SQL-03: MySQL connection hardening (A02:2025) -----------

    public function test_mysql_connection_enables_strict_sql_modes(): void
    {
        $modes = config('database.connections.mysql.modes');

        $this->assertTrue(config('database.connections.mysql.strict'));
        $this->assertContains('ONLY_FULL_GROUP_BY', $modes);
        $this->assertContains('STRICT_TRANS_TABLES', $modes);
    }

    public function test_mysql_connection_uses_utf8mb4(): void
    {
        $this->assertSame('utf8mb4', config('database.connections.mysql.charset'));
        $this->assertSame('utf8mb4_0900_ai_ci', config('database.connections.mysql.collation'));
        $this->assertSame('InnoDB', config('database.connections.mysql.engine'));
    }

    // --- AUTH-01: mass assignment (A01:2025, CWE-915) ---------------------

    public function test_models_declare_a_fillable_whitelist(): void
    {
        foreach ([new Article, new User] as $model) {
            $this->assertNotEmpty(
                $model->getFillable(),
                get_class($model) . ' has no $fillable whitelist'
            );
        }
    }

    public function test_id_cannot_be_mass_assigned(): void
    {
        $author = User::factory()->create();

        $article = Article::create([
            'id' => 9999,
            'user_id' => $author->id,
            'title' => 'Mass assignment attempt',
            'content' => 'body',
            'status' => 'published',
        ]);

        $this->assertNotSame(9999, $article->id);
    }

    // --- AUTH-02: policy enforcement (A01:2025, CWE-285) ------------------

    public function test_draft_article_is_hidden_from_other_users(): void
    {
        $author = User::factory()->create();
        $intruder = User::factory()->create();
        $draft = Article::factory()->draft()->create(['user_id' => $author->id]);

        $response = $this->actingAs($intruder)->getJson("/api/articles/{$draft->id}");

        $response->assertStatus(403);
    }

    public function test_author_can_read_their_own_draft(): void
    {
        $author = User::factory()->create();
        $draft = Article::factory()->draft()->create(['user_id' => $author->id]);

        $this->actingAs($author)
            ->getJson("/api/articles/{$draft->id}")
            ->assertStatus(200);
    }

    public function test_user_cannot_delete_another_users_article(): void
    {
        $author = User::factory()->create();
        $intruder = User::factory()->create();
        $article = Article::factory()->create(['user_id' => $author->id]);

        $this->actingAs($intruder)
            ->deleteJson("/api/articles/{$article->id}")
            ->assertStatus(403);

        $this->assertDatabaseHas('articles', ['id' => $article->id]);
    }

    public function test_author_can_delete_their_own_article(): void
    {
        $author = User::factory()->create();
        $article = Article::factory()->create(['user_id' => $author->id]);

        $this->actingAs($author)
            ->deleteJson("/api/articles/{$article->id}")
            ->assertStatus(200);

        $this->assertDatabaseMissing('articles', ['id' => $article->id]);
    }

    // --- AUTH-03: input validation (A05:2025, CWE-20) ---------------------

    #[DataProvider('invalidPayloads')]
    public function test_invalid_payloads_are_rejected(array $payload): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)
            ->postJson('/api/articles', $payload)
            ->assertStatus(422);
    }

    public static function invalidPayloads(): array
    {
        return [
            'missing title' => [['content' => 'body']],
            'title too short' => [['title' => 'ab', 'content' => 'body']],
            'title too long' => [['title' => str_repeat('a', 256), 'content' => 'body']],
            'missing content' => [['title' => 'A valid title']],
            'bad status' => [['title' => 'A valid title', 'content' => 'body', 'status' => 'wat']],
        ];
    }

    public function test_valid_payload_is_accepted(): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)
            ->postJson('/api/articles', [
                'title' => 'A perfectly valid title',
                'content' => 'Body content.',
                'status' => 'draft',
            ])
            ->assertStatus(201);
    }

    // --- CONC-01 / CONC-02 / CONC-03: integrity (A08:2025) ----------------

    public function test_writes_are_wrapped_in_a_retrying_transaction(): void
    {
        $source = file_get_contents(app_path('Http/Controllers/ArticleController.php'));

        $this->assertStringContainsString('DB::transaction(', $source);
        $this->assertMatchesRegularExpression('/attempts:\s*[2-9]/', $source);
    }

    public function test_status_and_created_at_are_indexed_together(): void
    {
        $indexes = collect(Schema::getIndexes('articles'))
            ->map(fn ($i) => $i['columns'])
            ->filter(fn ($cols) => in_array('status', $cols, true) && in_array('created_at', $cols, true));

        $this->assertNotEmpty($indexes, 'no compound index on (status, created_at)');
    }

    public function test_deleting_a_user_cascades_to_their_articles(): void
    {
        $author = User::factory()->create();
        Article::factory()->count(3)->create(['user_id' => $author->id]);

        DB::statement('PRAGMA foreign_keys = ON');
        $author->delete();

        $this->assertSame(0, Article::where('user_id', $author->id)->count());
    }

    // --- OPS-01: liveness probe (A10:2025) --------------------------------

    public function test_health_endpoint_reports_ok(): void
    {
        $this->getJson('/healthz')
            ->assertStatus(200)
            ->assertJson(['status' => 'ok', 'app' => 'laravel-mysql']);
    }

    // --- OPS-02 / CI-01: container and pipeline (A02/A03:2025) ------------

    public function test_dockerfile_runs_as_a_non_root_user(): void
    {
        $dockerfile = file_get_contents(base_path('Dockerfile'));

        $this->assertMatchesRegularExpression(
            '/^USER\s+(?!root)\S+/m',
            $dockerfile,
            'Dockerfile has no non-root USER directive'
        );
    }

    public function test_env_example_contains_no_real_secret(): void
    {
        $env = file_get_contents(base_path('.env.example'));

        $this->assertStringNotContainsString("\u{FEFF}", $env, '.env.example starts with a BOM');
        $this->assertMatchesRegularExpression('/^APP_KEY=\s*$/m', $env, 'APP_KEY must ship empty');
    }
}
