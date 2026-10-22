---
name: "sqlalchemy-async-migrations"
description: "Configure SQLAlchemy 2.0 asyncpg connection pools, write bidirectional Alembic migrations, and optimize queries with composite indexes."
---

# Skill: SQLAlchemy 2.0 Async Migrations & Connection Pooling

Use this skill to configure database connection pools, manage Alembic migrations, and optimize queries.

## 1. Asyncpg Pool Configuration
Configure connection pooling parameters in your database provider:
```python
engine = create_async_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)
```

## 2. Generating Alembic Migrations
Generate a new schema migration from DeclarativeBase metadata:
```bash
alembic revision --autogenerate -m "create_items_table"
```

Verify migration file contains both `upgrade()` and `downgrade()` functions:
```python
def upgrade() -> None:
    op.create_table(
        'items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_items_tenant', 'items', ['tenant_id'])

def downgrade() -> None:
    op.drop_index('idx_items_tenant', table_name='items')
    op.drop_table('items')
```
