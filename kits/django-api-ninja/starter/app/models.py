from django.conf import settings
from django.db import models


class ApiToken(models.Model):
    """Bearer credential carrying the tenant a request is allowed to see.

    Resolved by ApiKeyAuth and attached to request.auth, so every query can be
    scoped without the handler having to re-derive the caller's tenant.
    """

    key = models.CharField(max_length=64, unique=True, db_index=True)
    tenant_id = models.CharField(max_length=64, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="api_tokens"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} @ {self.tenant_id}"


class Project(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    tenant_id = models.CharField(max_length=64, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant_id", "is_active", "-created_at"]),
        ]
        # Slugs are unique per tenant, not globally: two tenants may both
        # have a project called "internal" without colliding.
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "slug"], name="uniq_project_slug_per_tenant"
            ),
        ]

    def __str__(self):
        return self.name
