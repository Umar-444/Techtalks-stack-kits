from litestar import Litestar, get
from litestar.response import Response

@get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "framework": "litestar", "typing": "strict"}

app = Litestar(route_handlers=[health_check])
