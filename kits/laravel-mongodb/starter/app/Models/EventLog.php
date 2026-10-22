<?php

declare(strict_types=1);

namespace App\Models;

use MongoDB\Laravel\Eloquent\Model;

class EventLog extends Model
{
    protected $connection = 'mongodb';
    protected $collection = 'event_logs';

    protected $fillable = [
        'user_id',
        'category',
        'action',
        'severity',
        'latency_ms',
        'metadata',
    ];

    protected $casts = [
        'latency_ms' => 'integer',
        'metadata' => 'array',
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
    ];
}
