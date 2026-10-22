<?php

use App\Http\Controllers\ArticleController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

// Health check endpoint
Route::get('/healthz', function () {
    return response()->json([
        'status' => 'ok',
        'app' => 'laravel-mysql',
        'version' => '1.0.0',
        'database' => 'mysql-8.4',
    ]);
});

Route::apiResource('api/articles', ArticleController::class);
