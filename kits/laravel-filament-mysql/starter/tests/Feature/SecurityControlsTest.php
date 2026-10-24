<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Filament\Resources\CustomerResource\Pages\CreateCustomer;
use App\Filament\Resources\CustomerResource\Pages\ListCustomers;
use App\Models\Customer;
use App\Models\User;
use Filament\Facades\Filament;
use Filament\Pages\Auth\Login;
use Illuminate\Cookie\Middleware\EncryptCookies;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Hash;
use Livewire\Livewire;
use Tests\TestCase;

/**
 * Controls declared in security/checks.json that can be exercised without a
 * MySQL server. Runs on SQLite in-memory; MySQL-specific settings are asserted
 * against the shipped connection config, not a live server.
 */
class SecurityControlsTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        Filament::setCurrentPanel(Filament::getPanel('admin'));
    }

    // SEC-01
    public function test_env_example_ships_no_real_secret(): void
    {
        $env = file_get_contents(base_path('.env.example'));

        $this->assertStringNotContainsString("\u{FEFF}", $env);
        $this->assertMatchesRegularExpression('/^APP_KEY=\s*$/m', $env);
    }

    // SEC-02
    public function test_dockerfile_runs_as_non_root(): void
    {
        $this->assertMatchesRegularExpression('/^USER\s+(?!root\b|0\b)\S+/m', file_get_contents(base_path('Dockerfile')));
    }

    // SEC-03
    public function test_unauthenticated_visitor_is_redirected_to_login(): void
    {
        $this->get('/admin/customers')->assertRedirect('/admin/login');
    }

    public function test_user_only_sees_own_team_in_the_list(): void
    {
        $mine = Customer::factory()->create(['team_id' => 1]);
        $theirs = Customer::factory()->create(['team_id' => 2]);

        $this->actingAs(User::factory()->create(['team_id' => 1]));

        Livewire::test(ListCustomers::class)
            ->assertCanSeeTableRecords([$mine])
            ->assertCanNotSeeTableRecords([$theirs]);
    }

    public function test_admin_sees_every_team(): void
    {
        $a = Customer::factory()->create(['team_id' => 1]);
        $b = Customer::factory()->create(['team_id' => 2]);

        $this->actingAs(User::factory()->admin()->create());

        Livewire::test(ListCustomers::class)->assertCanSeeTableRecords([$a, $b]);
    }

    public function test_user_cannot_open_other_teams_customer(): void
    {
        $theirs = Customer::factory()->create(['team_id' => 2]);

        $this->actingAs(User::factory()->create(['team_id' => 1]))
            ->get("/admin/customers/{$theirs->id}/edit")
            ->assertStatus(404);
    }

    public function test_user_can_open_own_teams_customer(): void
    {
        $mine = Customer::factory()->create(['team_id' => 1]);

        $this->actingAs(User::factory()->create(['team_id' => 1]))
            ->get("/admin/customers/{$mine->id}/edit")
            ->assertOk();
    }

    public function test_created_customer_is_forced_into_creators_team(): void
    {
        $this->actingAs(User::factory()->create(['team_id' => 7]));

        Livewire::test(CreateCustomer::class)
            ->fillForm(['name' => 'Fresh Co', 'email' => 'fresh@example.test', 'status' => 'active'])
            ->call('create')
            ->assertHasNoFormErrors();

        $this->assertSame(7, Customer::where('email', 'fresh@example.test')->firstOrFail()->team_id);
    }

    public function test_non_admin_cannot_delete(): void
    {
        $customer = Customer::factory()->create(['team_id' => 1]);

        $this->assertFalse(User::factory()->create(['team_id' => 1])->can('delete', $customer));
        $this->assertTrue(User::factory()->admin()->create()->can('delete', $customer));
    }

    // SEC-04
    public function test_fulltext_term_is_bound(): void
    {
        $query = Customer::fullTextSearch("'; DROP TABLE customers; --");

        $this->assertStringNotContainsString('DROP TABLE', $query->toSql());
        $this->assertCount(1, $query->getBindings());
    }

    // SEC-05
    public function test_mysql_strict_mode_configured(): void
    {
        $this->assertTrue(config('database.connections.mysql.strict'));
        $this->assertContains('STRICT_TRANS_TABLES', config('database.connections.mysql.modes'));
        $this->assertContains('ONLY_FULL_GROUP_BY', config('database.connections.mysql.modes'));
    }

    // SEC-06
    public function test_role_and_team_cannot_be_mass_assigned(): void
    {
        $user = (new User)->fill(['name' => 'x', 'role' => 'admin', 'team_id' => 99]);

        $this->assertNull($user->role);
        $this->assertNull($user->team_id);
        $this->assertNotEmpty((new Customer)->getFillable());
    }

    // SEC-07
    public function test_panel_middleware_includes_csrf_and_encrypted_cookies(): void
    {
        $middleware = Filament::getPanel('admin')->getMiddleware();

        $this->assertContains(VerifyCsrfToken::class, $middleware);
        $this->assertContains(EncryptCookies::class, $middleware);
    }

    // SEC-08
    public function test_session_cookie_is_hardened(): void
    {
        $this->assertTrue(config('session.http_only'));
        $this->assertSame('lax', config('session.same_site'));
        $this->assertTrue(config('session.secure'));
    }

    // SEC-09
    public function test_passwords_use_argon2id(): void
    {
        $this->assertSame('argon2id', config('hashing.driver'));
        $this->assertSame(65536, config('hashing.argon.memory'));
        $this->assertStringStartsWith('$argon2id$', Hash::make('secret-value'));
    }

    // SEC-10
    public function test_login_is_rate_limited(): void
    {
        $component = Livewire::test(Login::class)
            ->fillForm(['email' => 'nobody@example.test', 'password' => 'wrong-password']);

        for ($i = 0; $i < 5; $i++) {
            $component->call('authenticate')->assertNotNotified();
        }

        $component->call('authenticate')->assertNotified();
    }
}
