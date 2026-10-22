<?php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\ProjectController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes - v1
|--------------------------------------------------------------------------
*/

Route::prefix('v1')->group(function () {
    // Public authentication routes with strict throttle
    Route::prefix('auth')->middleware('throttle:10,1')->group(function () {
        Route::post('token', [AuthController::class, 'login']);
    });

    // Authenticated API routes
    Route::middleware(['auth:sanctum', 'throttle:60,1'])->group(function () {
        Route::prefix('auth')->group(function () {
            Route::get('me', [AuthController::class, 'me']);
            Route::post('revoke', [AuthController::class, 'revoke']);
        });

        // Read routes
        Route::middleware('ability:projects:read')->group(function () {
            Route::get('projects', [ProjectController::class, 'index']);
            Route::get('projects/{project}', [ProjectController::class, 'show']);
        });

        // Write routes
        Route::middleware('ability:projects:write')->group(function () {
            Route::post('projects', [ProjectController::class, 'store']);
            Route::put('projects/{project}', [ProjectController::class, 'update']);
            Route::delete('projects/{project}', [ProjectController::class, 'destroy']);
        });
    });

    Route::get('health', function () {
        return response()->json(['status' => 'ok', 'timestamp' => now()->toIso8601String()]);
    });
});
