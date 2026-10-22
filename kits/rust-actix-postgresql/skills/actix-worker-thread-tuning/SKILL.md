---
name: actix-worker-thread-tuning
description: Tune Actix Web worker threads, Tokio threadpool allocations, and SeaORM connection limits for peak throughput.
---

# Actix Worker Thread & Concurrency Tuning

## Actix Web Worker Architecture
Actix Web assigns an independent single-threaded event loop to each worker thread. By default, it allocates workers equal to logical CPU cores.

```rust
HttpServer::new(move || {
    App::new()
        .app_data(state.clone())
        .wrap(Logger::default())
        .configure(routes::config)
})
.workers(num_cpus::get()) // Tune explicitly based on deployment core quotas
.bind(("0.0.0.0", port))?
.run()
.await
```

## Connection Pool Sizing Rules
To prevent thread starvation and PostgreSQL backend saturation:
- Max Connections = `(Actix Workers * 3) + 5`
- Acquire Timeout: Set to `3 seconds` to fail fast under overload instead of piling up unserviced requests.
- Connect Timeout: Set to `5 seconds` to handle cold network links.

```rust
let mut opt = ConnectOptions::new(&database_url);
opt.max_connections(25)
   .min_connections(5)
   .connect_timeout(Duration::from_secs(5))
   .acquire_timeout(Duration::from_secs(3))
   .idle_timeout(Duration::from_secs(600))
   .sqlx_logging(true)
   .sqlx_logging_level(log::LevelFilter::Debug);

let db = Database::connect(opt).await?;
```
