<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Filament\Resources\CustomerResource\Pages\CreateCustomer;
use App\Filament\Resources\CustomerResource\Pages\ListCustomers;
use App\Models\Customer;
use App\Models\User;
use Filament\Facades\Filament;
use Filament\Pages\Auth\Login;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Livewire\Livewire;
use Tests\TestCase;

/**
 * Controls declared in security/checks.json that can be exercised without a
 * PostgreSQL server. Runs on SQLite in-memory. CI-01..03 (Gitleaks, Semgrep,
 * composer audit) are pipeline gates and are not exercised here.
 */
class SecurityControlsTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        Filament::setCurrentPanel(Filament::getPanel('admin'));
    }

    // AUTH-01
    public function test_passwords_use_argon2id_with_a_strong_work_factor(): void
    {
        $this->assertSame('argon2id', config('hashing.driver'));
        $this->assertGreaterThanOrEqual(65536, config('hashing.argon.memory'));
        $this->assertStringStartsWith('$argon2id$', Hash::make('secret-value'));
    }

    // AUTH-02
    public function test_session_cookie_flags_are_hardened(): void
    {
        $this->assertTrue(config('session.secure'));
        $this->assertTrue(config('session.http_only'));
        $this->assertSame('lax', config('session.same_site'));
    }

    // AUTH-03
    public function test_session_is_regenerated_on_login(): void
    {
        $user = User::factory()->create(['email' => 'login@example.test', 'password' => 'correct-horse']);

        $component = Livewire::test(Login::class);
        $before = session()->getId();

        $component
            ->fillForm(['email' => 'login@example.test', 'password' => 'correct-horse'])
            ->call('authenticate')
            ->assertHasNoFormErrors();

        $this->assertAuthenticatedAs($user);
        $this->assertNotSame($before, session()->getId());
    }

    // AUTH-04
    public function test_login_is_rate_limited(): void
    {
        $component = Livewire::test(Login::class)
            ->fillForm(['email' => 'nobody@example.test', 'password' => 'wrong-password']);

        for ($i = 0; $i < 5; $i++) {
            $component->call('authenticate')->assertNotNotified();
        }

        $component->call('authenticate')->assertNotified();
    }

    // AUTHZ-01
    public function test_user_only_sees_own_customers_in_the_list(): void
    {
        $me = User::factory()->create();
        $mine = Customer::factory()->create(['user_id' => $me->id]);
        $theirs = Customer::factory()->create();

        $this->actingAs($me);

        Livewire::test(ListCustomers::class)
            ->assertCanSeeTableRecords([$mine])
            ->assertCanNotSeeTableRecords([$theirs]);
    }

    public function test_unauthenticated_visitor_is_redirected_to_login(): void
    {
        $this->get('/admin/customers')->assertRedirect('/admin/login');
    }

    public function test_created_customer_is_owned_by_the_creator(): void
    {
        $me = User::factory()->create();
        $this->actingAs($me);

        Livewire::test(CreateCustomer::class)
            ->fillForm(['name' => 'Fresh Co', 'email' => 'fresh@example.test', 'status' => 'active'])
            ->call('create')
            ->assertHasNoFormErrors();

        $this->assertSame($me->id, Customer::where('email', 'fresh@example.test')->firstOrFail()->user_id);
    }

    // AUTHZ-02
    public function test_policy_blocks_other_users_for_every_mutation(): void
    {
        $owner = User::factory()->create();
        $intruder = User::factory()->create();
        $customer = Customer::factory()->create(['user_id' => $owner->id]);

        foreach (['view', 'update', 'delete'] as $ability) {
            $this->assertTrue($owner->can($ability, $customer), "owner should be able to {$ability}");
            $this->assertFalse($intruder->can($ability, $customer), "intruder must not {$ability}");
        }
    }

    public function test_intruder_cannot_open_the_edit_page(): void
    {
        $customer = Customer::factory()->create();

        $this->actingAs(User::factory()->create())
            ->get("/admin/customers/{$customer->id}/edit")
            ->assertStatus(404);
    }

    // DATA-01
    public function test_table_search_treats_injection_as_data(): void
    {
        $me = User::factory()->create();
        $mine = Customer::factory()->create(['user_id' => $me->id, 'name' => 'Legit Customer']);
        $this->actingAs($me);

        Livewire::test(ListCustomers::class)
            ->searchTable("' OR 1=1 --")
            ->assertCanNotSeeTableRecords([$mine]);

        Livewire::test(ListCustomers::class)
            ->searchTable('Legit')
            ->assertCanSeeTableRecords([$mine]);
    }

    // DATA-02
    public function test_customer_name_is_escaped_in_the_table(): void
    {
        $me = User::factory()->create();
        Customer::factory()->create(['user_id' => $me->id, 'name' => '<script>alert(1)</script>']);
        $this->actingAs($me);

        Livewire::test(ListCustomers::class)
            ->assertDontSeeHtml('<script>alert(1)</script>')
            ->assertSee('alert(1)');
    }

    // DATA-03
    public function test_panel_keeps_csrf_verification(): void
    {
        $this->assertContains(VerifyCsrfToken::class, Filament::getPanel('admin')->getMiddleware());
    }

    // Supporting invariants
    public function test_primary_keys_are_uuids(): void
    {
        $this->assertTrue(Str::isUuid((string) User::factory()->create()->id));
        $this->assertTrue(Str::isUuid((string) Customer::factory()->create()->id));
    }

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
