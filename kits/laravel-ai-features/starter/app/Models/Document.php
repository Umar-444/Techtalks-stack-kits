<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

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

    /** Restrict a query to one tenant (SEC-05). */
    public function scopeForTenant(Builder $query, int $tenantId): Builder
    {
        return $query->where('tenant_id', $tenantId);
    }

    /**
     * Cosine-distance nearest neighbours (pgvector `<=>`).
     *
     * The tenant is a required argument, so a semantic search can never run
     * across tenants by accident (SEC-05). The vector is passed as a bound
     * parameter, never interpolated (SEC-04).
     */
    public function scopeCosineSearch(Builder $query, array $vector, int $tenantId, int $limit = 5): Builder
    {
        $vectorJson = json_encode(array_map('floatval', $vector));

        return $query->forTenant($tenantId)
            ->selectRaw('*, (embedding <=> ?) as distance', [$vectorJson])
            ->orderByRaw('embedding <=> ?', [$vectorJson])
            ->limit(max(1, min($limit, 50)));
    }
}
