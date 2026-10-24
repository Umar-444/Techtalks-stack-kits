<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Models\Customer;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class CustomerResourceTest extends TestCase
{
    use RefreshDatabase;

    public function test_healthz_endpoint_returns_ok(): void
    {
        $this->get('/healthz')
            ->assertStatus(200)
            ->assertJson(['status' => 'ok', 'app' => 'laravel-filament-postgresql']);
    }

    public function test_user_cannot_view_another_users_customer(): void
    {
        $userA = User::factory()->create();
        $userB = User::factory()->create();
        $customerA = Customer::factory()->create(['user_id' => $userA->id]);

        $this->assertFalse($userB->can('view', $customerA));
        $this->assertTrue($userA->can('view', $customerA));
    }

    public function test_deleting_a_user_cascades_to_their_customers(): void
    {
        $user = User::factory()->create();
        Customer::factory()->count(2)->create(['user_id' => $user->id]);

        $user->delete();

        $this->assertSame(0, Customer::count());
    }
}
