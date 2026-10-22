<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\EventLog;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $user = User::firstOrCreate(
            ['email' => 'admin@example.com'],
            [
                'name' => 'Demo Admin',
                'password' => Hash::make('Secret123!'),
            ]
        );

        EventLog::firstOrCreate(
            ['action' => 'user_login_success'],
            [
                'user_id' => (string) $user->id,
                'category' => 'auth',
                'severity' => 'low',
                'latency_ms' => 45,
                'metadata' => ['ip' => '127.0.0.1', 'auth_type' => 'password'],
            ]
        );

        EventLog::firstOrCreate(
            ['action' => 'aggregation_query_executed'],
            [
                'user_id' => (string) $user->id,
                'category' => 'analytics',
                'severity' => 'low',
                'latency_ms' => 12,
                'metadata' => ['pipeline_stages' => 3],
            ]
        );
    }
}
