from dataclasses import dataclass
from datetime import datetime

from app.lib.routeros.domain.entities import SystemResource
from app.lib.routeros.domain.repositories import (
    SystemResourceRepository,
)
from app.lib.routeros.types import ConnectionConfig


@dataclass
class SystemResourceResponse:
    """Response object for system resource operations."""

    success: bool
    data: SystemResource | None = None
    error_message: str | None = None
    timestamp: datetime = datetime.now()


class GetSystemResourceUseCase:
    """Use case for retrieving system resource information."""

    def __init__(self, system_resource_repo: SystemResourceRepository):
        self._system_resource_repo = system_resource_repo

    async def execute(self, request: ConnectionConfig) -> SystemResourceResponse:
        """
        Execute the use case to get system resource information.

        Args:
            request: SystemResourceRequest containing connection details

        Returns:
            SystemResourceResponse with system resource data or error
        """
        try:
            # Check connection first
            is_connected = await self._system_resource_repo.check_connection()
            if not is_connected:
                return SystemResourceResponse(
                    success=False,
                    error_message=f"Unable to connect to router at {request.host}",
                )

            # Get system resource data
            system_resource = await self._system_resource_repo.get_system_resource()
            if not system_resource:
                return SystemResourceResponse(
                    success=False,
                    error_message="Failed to retrieve system resource data",
                )
            return SystemResourceResponse(success=True, data=system_resource)

        except Exception as e:
            return SystemResourceResponse(
                success=False, error_message=f"An error occurred: {str(e)}"
            )


class MonitorSystemHealthUseCase:
    """Use case for monitoring system health and detecting critical conditions."""

    def __init__(self, system_resource_repo: SystemResourceRepository):
        self._system_resource_repo = system_resource_repo

    async def execute(self, request: ConnectionConfig) -> SystemResourceResponse:
        """
        Execute system health monitoring.

        Args:
            request: SystemResourceRequest containing connection details

        Returns:
            SystemResourceResponse with health analysis
        """
        try:
            # Check connection first
            is_connected = await self._system_resource_repo.check_connection()
            if not is_connected:
                return SystemResourceResponse(
                    success=False,
                    error_message=f"Unable to connect to router at {request.host}",
                )

            system_resource = await self._system_resource_repo.get_system_resource()
            if not system_resource:
                return SystemResourceResponse(
                    success=False,
                    error_message="Failed to retrieve system resource data for health monitoring",
                )

            # Add health warnings to the response
            warnings = []
            if system_resource.is_memory_critical:
                warnings.append(
                    f"Critical memory usage: {system_resource.memory_usage_percentage:.1f}%"
                )

            if system_resource.is_cpu_critical:
                warnings.append(f"Critical CPU usage: {system_resource.cpu_load}%")

            error_message = "; ".join(warnings) if warnings else None

            return SystemResourceResponse(
                success=True,
                data=system_resource,
                error_message=error_message,  # Using error_message for warnings
            )

        except Exception as e:
            return SystemResourceResponse(
                success=False, error_message=f"Health monitoring failed: {str(e)}"
            )
