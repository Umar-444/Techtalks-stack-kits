<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Builder;

class Document extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
        'content',
        'embedding',
        'tenant_id',
    ];

    protected function casts(): array
    {
        return [
            'embedding' => 'array',
        ];
    }

    public function scopeCosineSearch(Builder $query, array $vector, int $limit = 5): Builder
    {
        $vectorJson = json_encode($vector);
        return $query->selectRaw('*, (embedding <=> ?) as distance', [$vectorJson])
                     ->orderByRaw('embedding <=> ?', [$vectorJson])
                     ->limit($limit);
    }
}
