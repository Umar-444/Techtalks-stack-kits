from ninja.security import HttpBearer

from app.models import ApiToken


class ApiKeyAuth(HttpBearer):
    """Resolves a Bearer token to its ApiToken row.

    Returning the token (not the user) puts tenant_id on request.auth, which
    is what the handlers scope their queries by. An unknown or deactivated
    token returns None and Django Ninja answers 401.
    """

    def authenticate(self, request, token):
        return (
            ApiToken.objects.select_related("user")
            .filter(key=token, is_active=True)
            .first()
        )


auth = ApiKeyAuth()
