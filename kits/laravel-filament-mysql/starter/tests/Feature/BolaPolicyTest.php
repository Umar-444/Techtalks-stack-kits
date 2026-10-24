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
        $admin = (new User)->forceFill(['role' => 'admin', 'team_id' => 1]);
        $customer = (new Customer)->forceFill(['team_id' => 2]);

        $this->assertTrue((new CustomerPolicy)->view($admin, $customer));
    }

    public function test_regular_user_cannot_view_customer_from_different_team(): void
    {
        $user = (new User)->forceFill(['role' => 'user', 'team_id' => 1]);
        $customer = (new Customer)->forceFill(['team_id' => 2]);

        $this->assertFalse((new CustomerPolicy)->view($user, $customer));
    }

    public function test_regular_user_can_view_customer_in_own_team(): void
    {
        $user = (new User)->forceFill(['role' => 'user', 'team_id' => 3]);
        $customer = (new Customer)->forceFill(['team_id' => 3]);

        $this->assertTrue((new CustomerPolicy)->view($user, $customer));
    }
}
