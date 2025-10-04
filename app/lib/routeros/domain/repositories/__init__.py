from abc import ABC, abstractmethod

from app.lib.routeros.domain.entities import RouterInfo, SystemResource


class SystemResourceRepository(ABC):
    """Abstract repository interface for system resource operations."""

    @abstractmethod
    async def get_system_resource(self) -> SystemResource | None:
        """Get system resource information from a router."""
        pass

    @abstractmethod
    async def check_connection(self) -> bool:
        """Check if connection to router is available."""
        pass


class RouterInfoRepository(ABC):
    """Abstract repository interface for router information operations."""

    @abstractmethod
    async def get_router_info(self) -> RouterInfo | None:
        """Get router information."""
        pass

    @abstractmethod
    async def update_router_info(self, router_info: RouterInfo) -> bool:
        """Update router information."""
        pass
