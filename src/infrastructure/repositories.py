from typing import Dict, Optional
from datetime import datetime

from src.domain.entities import RouterInfo
from src.domain.repositories import RouterInfoRepository


class InMemoryRouterInfoRepository(RouterInfoRepository):
    """In-memory implementation of RouterInfoRepository for demonstration."""
    
    def __init__(self):
        self._routers: Dict[str, RouterInfo] = {}

    async def get_router_info(self, host: str) -> Optional[RouterInfo]:
        """Get router information from memory."""
        return self._routers.get(host)

    async def update_router_info(self, router_info: RouterInfo) -> bool:
        """Update router information in memory."""
        try:
            router_info.last_updated = datetime.now()
            self._routers[router_info.host] = router_info
            return True
        except Exception:
            return False
    
    def list_all_routers(self) -> Dict[str, RouterInfo]:
        """List all stored router information."""
        return self._routers.copy()