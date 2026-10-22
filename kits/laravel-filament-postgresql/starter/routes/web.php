<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect('/admin');
});

Route::get('/healthz', function () {
    return response()->json([
        'status' => 'ok',
        'app' => 'laravel-filament-postgresql',
        'version' => '1.0.0',
        'php' => PHP_VERSION,
        'database' => 'connected',
    ]);
});
