<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class AuthApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_login_and_receive_token(): void
    {
        $user = User::factory()->create([
            'email' => 'developer@example.com',
            'password' => bcrypt('StrongPassword123!'),
        ]);

        $response = $this->postJson('/api/v1/auth/token', [
            'email' => 'developer@example.com',
            'password' => 'StrongPassword123!',
            'device_name' => 'integration-test',
        ]);

        $response->assertStatus(200)
            ->assertJsonStructure([
                'token_type',
                'access_token',
                'abilities',
                'user' => ['id', 'name', 'email'],
            ]);
    }

    public function test_invalid_credentials_returns_422(): void
    {
        $response = $this->postJson('/api/v1/auth/token', [
            'email' => 'unknown@example.com',
            'password' => 'WrongPassword!',
        ]);

        $response->assertStatus(422);
    }
}
