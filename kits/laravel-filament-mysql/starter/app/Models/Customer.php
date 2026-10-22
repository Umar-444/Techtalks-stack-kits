<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Builder;

class Customer extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'email',
        'company_name',
        'status',
        'team_id',
    ];

    public function scopeFullTextSearch(Builder $query, string $term): Builder
    {
        return $query->whereRaw(
            "MATCH(name, email, company_name) AGAINST(? IN BOOLEAN MODE)",
            [$term . '*']
        );
    }
}
