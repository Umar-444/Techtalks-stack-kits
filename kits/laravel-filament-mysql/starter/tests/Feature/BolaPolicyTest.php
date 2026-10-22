<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Models\Customer;
use App\Models\User;
use App\Policies\CustomerPolicy;
use Tests\TestCase;

class BolaPolicyTest extends TestCase
{
    public function test_admin_can_view_any_customer(): void
    {
        $admin = new User(['role' => 'admin', 'team_id' => 1]);
        $customer = new Customer(['team_id' => 2]);

        $policy = new CustomerPolicy();
        $this->assertTrue($policy->view($admin, $customer));
    }

    public function test_regular_user_cannot_view_customer_from_different_team(): void
    {
        $user = new User(['role' => 'user', 'team_id' => 1]);
        $customer = new Customer(['team_id' => 2]);

        $policy = new CustomerPolicy();
        $this->assertFalse($policy->view($user, $customer));
    }
}
