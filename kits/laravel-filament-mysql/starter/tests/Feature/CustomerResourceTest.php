<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Models\Customer;
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

    public function test_fulltext_scope_binds_the_search_term(): void
    {
        // MATCH ... AGAINST is MySQL-only; SQLite cannot execute it, so assert
        // the generated SQL instead of running it.
        $query = Customer::fullTextSearch("x') OR 1=1 --");

        $this->assertStringContainsString('MATCH(name, email, company_name) AGAINST(? IN BOOLEAN MODE)', $query->toSql());
        $this->assertSame(["x') OR 1=1 --*"], $query->getBindings());
        $this->assertStringNotContainsString('OR 1=1', $query->toSql());
    }
}
