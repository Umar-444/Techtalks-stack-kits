<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Models\Customer;
use Illuminate\Database\Seeder;

class CustomerSeeder extends Seeder
{
    public function run(): void
    {
        $customers = [
            ['name' => 'Acme Corporation', 'email' => 'contact@acme.corp', 'company_name' => 'Acme Global', 'status' => 'active', 'team_id' => 1],
            ['name' => 'Cyberdyne Systems', 'email' => 'security@cyberdyne.ai', 'company_name' => 'Cyberdyne AI', 'status' => 'active', 'team_id' => 1],
            ['name' => 'Stark Enterprises', 'email' => 'tony@stark.tech', 'company_name' => 'Stark Industries', 'status' => 'active', 'team_id' => 2],
        ];

        foreach ($customers as $c) {
            Customer::firstOrCreate(['email' => $c['email']], $c);
        }
    }
}
