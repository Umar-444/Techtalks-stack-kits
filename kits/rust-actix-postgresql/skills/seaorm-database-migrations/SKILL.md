---
name: seaorm-database-migrations
description: Author, execute, and verify SeaORM database migrations with PostgreSQL schema safety.
---

# SeaORM Database Migrations Workflow

## Architecture
SeaORM manages migrations using a dedicated migration runner crate or module implementing `MigrationTrait`.

## Writing a Migration
In `migration/src/m20261022_000001_create_items_table.rs`:
```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(Items::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Items::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(Items::Title).string_len(150).not_null())
                    .col(ColumnDef::new(Items::Description).string_len(1000).null())
                    .col(
                        ColumnDef::new(Items::CreatedAt)
                            .timestamp_with_time_zone()
                            .not_null()
                            .default(Expr::current_timestamp()),
                    )
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .drop_table(Table::drop().table(Items::Table).to_owned())
            .await
    }
}

#[derive(DeriveIden)]
enum Items {
    Table,
    Id,
    Title,
    Description,
    CreatedAt,
}
```

## Running Migrations at Startup
In `src/main.rs`:
```rust
use sea_orm_migration::prelude::*;
use migration::Migrator;

Migrator::up(&db, None).await.expect("Failed to run database migrations");
```
