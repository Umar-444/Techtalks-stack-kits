<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Customer;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $admin = User::firstOrCreate(
            ['email' => 'admin@example.com'],
            [
                'name' => 'Demo Admin',
                'password' => Hash::make('Secret123!'),
            ]
        );

        Customer::firstOrCreate(
            ['email' => 'acme@example.com'],
            [
                'user_id' => $admin->id,
                'name' => 'Acme Corp',
                'company' => 'Acme Global',
                'status' => 'active',
                'metadata' => ['tier' => 'enterprise'],
            ]
        );
    }
}
