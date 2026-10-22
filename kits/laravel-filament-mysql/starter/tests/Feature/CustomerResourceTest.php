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

    public function test_it_returns_health_endpoint_cleanly(): void
    {
        $response = $this->get('/api/health');
        $response->assertStatus(200);
        $response->assertJson(['status' => 'ok', 'database' => 'mysql-8.4-innodb']);
    }

    public function test_mysql_fulltext_search_filters_customers(): void
    {
        Customer::create([
            'name' => 'Alpha Sentinel',
            'email' => 'alpha@security.io',
            'company_name' => 'Sentinel Corp',
            'status' => 'active',
            'team_id' => 1,
        ]);

        Customer::create([
            'name' => 'Beta Voyager',
            'email' => 'beta@travel.io',
            'company_name' => 'Voyager Ltd',
            'status' => 'active',
            'team_id' => 1,
        ]);

        $results = Customer::fullTextSearch('Sentinel')->get();
        $this->assertCount(1, $results);
        $this->assertEquals('Alpha Sentinel', $results->first()->name);
    }
}
