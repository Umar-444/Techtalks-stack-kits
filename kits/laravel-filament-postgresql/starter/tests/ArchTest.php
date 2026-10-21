<?php

declare(strict_types=1);

test('controllers do not access DB facade directly')
    ->expect('App\Http\Controllers')
    ->not->toUse('Illuminate\Support\Facades\DB');

test('all models use UUIDs')
    ->expect('App\Models')
    ->toUse('Illuminate\Database\Eloquent\Concerns\HasUuids');

test('no debugging calls remain in code')
    ->expect(['dd', 'dump', 'ray', 'var_dump'])
    ->not->toBeUsed();
