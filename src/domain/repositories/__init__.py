from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities import SystemResource, RouterInfo


class SystemResourceRepository(ABC):
    """Abstract repository interface for system resource operations."""
    
    @abstractmethod
    async def get_system_resource(self, host: str) -> Optional[SystemResource]:
        """Get system resource information from a router."""
        pass
    
    @abstractmethod
    async def check_connection(self, host: str) -> bool:
        """Check if connection to router is available."""
        pass


class RouterInfoRepository(ABC):
    """Abstract repository interface for router information operations."""
    
    @abstractmethod
    async def get_router_info(self, host: str) -> Optional[RouterInfo]:
        """Get router information."""
        pass
    
    @abstractmethod
    async def update_router_info(self, router_info: RouterInfo) -> bool:
        """Update router information."""
        pass