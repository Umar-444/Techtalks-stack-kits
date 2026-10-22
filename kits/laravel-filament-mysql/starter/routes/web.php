<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect('/admin');
});

Route::get('/api/health', function () {
    return response()->json([
        'status' => 'ok',
        'database' => 'mysql-8.4-innodb',
        'admin_panel' => 'filament-4',
    ]);
});
