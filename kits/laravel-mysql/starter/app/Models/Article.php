<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Article extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'title',
        'content',
        'status',
    ];

    protected $casts = [
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function scopePublished($query)
    {
        return $query->where('status', 'published');
    }

    /**
     * Full-text search. The term is always bound as a parameter, never
     * interpolated, on both branches (SQL-01).
     *
     * MATCH ... AGAINST is MySQL-only; SQLite (used by the test suite) falls
     * back to a bound LIKE so the same query path stays exercised in tests.
     */
    public function scopeSearch($query, string $term)
    {
        if (in_array($query->getConnection()->getDriverName(), ['mysql', 'mariadb'], true)) {
            return $query->whereRaw('MATCH(title, content) AGAINST(? IN BOOLEAN MODE)', [$term]);
        }

        return $query->where(function ($q) use ($term) {
            $q->where('title', 'like', '%' . $term . '%')
              ->orWhere('content', 'like', '%' . $term . '%');
        });
    }
}
