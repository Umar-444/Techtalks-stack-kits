<?php

namespace Tests\Feature;

use App\Models\User;
use App\Models\Customer;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class CustomerResourceTest extends TestCase
{
    use RefreshDatabase;

    public function test_healthz_endpoint_returns_ok(): void
    {
        $response = $this->get('/healthz');
        $response->assertStatus(200);
        $response->assertJson([
            'status' => 'ok',
            'app' => 'laravel-filament-postgresql'
        ]);
    }

    public function test_user_cannot_view_another_users_customer(): void
    {
        $userA = User::factory()->create();
        $userB = User::factory()->create();
        $customerA = Customer::create([
            'user_id' => $userA->id,
            'name' => 'Customer A',
            'email' => 'a@example.com',
            'status' => 'active'
        ]);

        $this->actingAs($userB);
        $this->assertFalse($userB->can('view', $customerA));
    }
}
