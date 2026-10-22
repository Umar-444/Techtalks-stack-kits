# SQLAlchemy 2.0 Async Sessions & Database Invariants

# 02 - SQLAlchemy 2.0 Async Sessions & Database Invariants

## 1. Async Engine & Session Lifecycle
- **Native AsyncIO Driver:** Standardize on `asyncpg` with SQLAlchemy 2.0:
  ```python
  from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

  engine = create_async_engine(
      settings.database_url,
      pool_size=20,
      max_overflow=10,
      pool_pre_ping=True,
      echo=False
  )
  session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
  ```
- **Session Injection:** Inject `AsyncSession` into request handlers and services via Litestar's DI. Ensure sessions are committed on success or rolled back automatically on unhandled exceptions.

## 2. Declarative Models & Indexing
- Define models inheriting from `sqlalchemy.orm.DeclarativeBase`:
  ```python
  from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
  from sqlalchemy import String, Boolean, DateTime, Index
  from datetime import datetime

  class Base(DeclarativeBase):
      pass

  class Item(Base):
      __tablename__ = "items"

      id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
      title: Mapped[str] = mapped_column(String(200), nullable=False)
      tenant_id: Mapped[str] = mapped_column(String(64), nullable=False)
      is_active: Mapped[bool] = mapped_column(Boolean, default=True)
      created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

      __table_args__ = (
          Index("idx_items_tenant_active", "tenant_id", "is_active"),
      )
  ```

## 3. Strict Parameterized Queries
- Always construct queries using SQLAlchemy 2.0 `select()` statements:
  ```python
  stmt = select(Item).where(Item.tenant_id == tenant_id, Item.is_active == True).order_by(Item.created_at.desc())
  result = await session.execute(stmt)
  items = result.scalars().all()
  ```
- Never construct raw SQL strings via interpolation (`f"SELECT * FROM items WHERE id = '{item_id}'"`).

## 4. Reversible Alembic Migrations
- Keep all database schema changes tracked inside versioned Alembic migrations.
- Verify migrations run bidirectionally: `alembic upgrade head` followed by `alembic downgrade -1`.
