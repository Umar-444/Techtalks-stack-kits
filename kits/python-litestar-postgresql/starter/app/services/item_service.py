from typing import List, Optional, Dict
from app.domain.schemas import ItemCreate, ItemResponse

class ItemService:
    def __init__(self):
        self._items: Dict[int, ItemResponse] = {}
        self._counter = 1

    async def create(self, data: ItemCreate) -> ItemResponse:
        item = ItemResponse(
            id=self._counter,
            title=data.title,
            tenant_id=data.tenant_id,
            description=data.description,
            is_active=True
        )
        self._items[self._counter] = item
        self._counter += 1
        return item

    async def list(self, tenant_id: Optional[str] = None) -> List[ItemResponse]:
        if tenant_id:
            return [item for item in self._items.values() if item.tenant_id == tenant_id and item.is_active]
        return [item for item in self._items.values() if item.is_active]

    async def get_by_id(self, item_id: int, tenant_id: str) -> Optional[ItemResponse]:
        item = self._items.get(item_id)
        if item and item.tenant_id == tenant_id and item.is_active:
            return item
        return None

item_service = ItemService()
