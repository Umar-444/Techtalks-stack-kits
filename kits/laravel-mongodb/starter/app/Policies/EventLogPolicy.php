<?php

declare(strict_types=1);

namespace App\Policies;

use App\Models\EventLog;
use App\Models\User;

class EventLogPolicy
{
    public function viewAny(User $user): bool
    {
        return true;
    }

    public function view(User $user, EventLog $event): bool
    {
        return (string) $user->id === (string) $event->user_id;
    }

    public function create(User $user): bool
    {
        return true;
    }

    public function update(User $user, EventLog $event): bool
    {
        return (string) $user->id === (string) $event->user_id;
    }

    public function delete(User $user, EventLog $event): bool
    {
        return (string) $user->id === (string) $event->user_id;
    }
}
