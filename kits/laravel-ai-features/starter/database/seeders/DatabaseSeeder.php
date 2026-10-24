<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $admin = User::firstOrNew(['email' => 'admin@techtalks.dev']);
        if (! $admin->exists) {
            $admin->forceFill([
                'name' => 'AI System Admin',
                'password' => Hash::make('password123'),
                'role' => 'admin',
                'team_id' => 1,
            ])->save();
        }

        $this->call(DocumentSeeder::class);
    }
}
