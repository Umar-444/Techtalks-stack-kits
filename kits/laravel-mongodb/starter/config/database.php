<?php

return [
    'default' => env('DB_CONNECTION', 'mongodb'),

    'connections' => [

        'mongodb' => [
            'driver' => 'mongodb',
            'dsn' => env('MONGODB_URI', 'mongodb://127.0.0.1:27017'),
            'database' => env('MONGODB_DATABASE', 'app_mongo'),
            // Bounded connection pool and timeouts so a slow or hostile
            // backend cannot hold the app open indefinitely (DATA-02).
            'options' => [
                'maxPoolSize' => (int) env('MONGODB_MAX_POOL_SIZE', 50),
                'serverSelectionTimeoutMS' => (int) env('MONGODB_SERVER_SELECTION_TIMEOUT_MS', 5000),
                'connectTimeoutMS' => (int) env('MONGODB_CONNECT_TIMEOUT_MS', 5000),
                'socketTimeoutMS' => (int) env('MONGODB_SOCKET_TIMEOUT_MS', 30000),
            ],
        ],

    ],

    'migrations' => [
        'table' => 'migrations',
        'update_date_on_publish' => true,
    ],
];
