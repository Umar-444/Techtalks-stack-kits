<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return response()->json(['name' => 'Laravel AI Features', 'status' => 'ready']);
});

Route::get('/api/health', function () {
    return response()->json([
        'status' => 'ok',
        'ai_provider' => 'mock-ready',
        'database' => 'postgresql-16-pgvector',
    ]);
});
