<?php

use App\Http\Controllers\EventLogController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect('/events');
});

Route::get('/events', [EventLogController::class, 'index']);
Route::post('/events', [EventLogController::class, 'store']);

Route::get('/healthz', function () {
    return response()->json([
        'status' => 'ok',
        'app' => 'laravel-mongodb',
        'version' => '1.0.0',
        'database' => 'connected',
        'driver' => 'mongodb',
    ]);
});
