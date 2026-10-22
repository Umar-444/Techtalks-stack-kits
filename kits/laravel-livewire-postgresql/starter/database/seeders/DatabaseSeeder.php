<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Task;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $user = User::firstOrCreate(
            ['email' => 'user@example.com'],
            [
                'name' => 'Demo User',
                'password' => Hash::make('Password123!'),
            ]
        );

        Task::firstOrCreate(
            ['title' => 'Set up Livewire 4 Component'],
            [
                'user_id' => $user->id,
                'description' => 'Test real-time component reactivity with PostgreSQL persistence.',
                'priority' => 'high',
                'is_completed' => false,
            ]
        );
    }
}
