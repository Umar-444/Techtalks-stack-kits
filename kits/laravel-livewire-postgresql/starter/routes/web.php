<?php

use App\Livewire\TaskManager;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect('/tasks');
});

Route::get('/tasks', TaskManager::class);

Route::get('/healthz', function () {
    return response()->json([
        'status' => 'ok',
        'app' => 'laravel-livewire-postgresql',
        'version' => '1.0.0',
        'php' => PHP_VERSION,
        'database' => 'connected',
    ]);
});
