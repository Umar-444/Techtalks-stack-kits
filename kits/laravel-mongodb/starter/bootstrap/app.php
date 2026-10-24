<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__ . '/../routes/web.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        //
    })
    ->withExceptions(function (Exceptions $exceptions) {
        // This kit exposes a JSON API only: unauthenticated callers get a 401
        // body rather than a redirect to a login page that does not exist.
        $exceptions->shouldRenderJsonWhen(fn () => true);
    })->create();
