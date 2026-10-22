# Weaviate Collections and Multi-Tenant Isolation

1. **Weaviate v4 Python Client**: All schema definitions and queries must utilize the `weaviate-client` v4 collection API (`client.collections.get(...)` and `client.collections.create(...)`). Legacy v3 methods (`client.schema.create_class`) are prohibited.
2. **Multi-Tenancy Configuration**: Enable multi-tenancy at collection creation time via `Configure.multi_tenancy(enabled=True)` whenever managing multiple client or user organizations.
3. **Tenant Scoping on Every Query**: Never execute a search query without explicit tenant context. Obtain tenant-scoped collection references via `collection.with_tenant(tenant_id)`.
4. **Property Indexing**: Configure vectorizer properties explicitly. Mark text chunks with `skip=False` for vector indexing and administrative metadata (UUIDs, timestamps) with `skip=True`.
5. **Connection Pooling and Lifecycle**: Manage Weaviate client lifecycle using context managers (`with weaviate.connect_to_custom(...)`) or FastAPI lifespan handlers. Never leak open gRPC channels.
