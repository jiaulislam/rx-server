import asyncio
from devtools import debug
from dotenv import load_dotenv
from os import environ
from src.application.use_cases import (
    GetSystemResourceUseCase,
    MonitorSystemHealthUseCase,
    SystemResourceRequest
)
from src.infrastructure.mikrotik import MikroTikSystemResourceRepository
from src.infrastructure.repositories import InMemoryRouterInfoRepository

load_dotenv(dotenv_path=".env")  # Load environment variables from .env file

class RouterMonitoringController:
    """Controller for router monitoring operations."""
    
    def __init__(self, host: str, username: str, password: str, port: int = 8728):
        # Initialize repositories
        self.system_resource_repo = MikroTikSystemResourceRepository(username, password, port)
        self.router_info_repo = InMemoryRouterInfoRepository()
        self._system_resource_request = SystemResourceRequest(
            host=host,
            username=username,
            password=password,
            port=port,
        )
        
        # Initialize use cases
        self.get_system_resource_use_case = GetSystemResourceUseCase(
            self.system_resource_repo,
            self.router_info_repo
        )
        self.monitor_health_use_case = MonitorSystemHealthUseCase(
            self.system_resource_repo
        )
    
    async def get_system_resource(self) -> None:
        """Get and display system resource information."""

        response = await self.get_system_resource_use_case.execute(self._system_resource_request)
        
        if response.success:
            print(f"✅ Successfully retrieved system resource data from {self._system_resource_request.host}")
            debug(response.data)
            
            if response.error_message:  # This would be warnings
                print(f"⚠️  Warnings: {response.error_message}")
        else:
            print(f"❌ Failed to retrieve system resource data: {response.error_message}")
    
    async def monitor_system_health(self) -> None:
        """Monitor system health and display warnings."""

        response = await self.monitor_health_use_case.execute(self._system_resource_request)
        
        if response.success:
            print(f"🔍 System health check for {self._system_resource_request.host}")

            if response.data:
                print(f"Memory Usage: {response.data.memory_usage_percentage:.1f}%")
                print(f"CPU Usage: {response.data.cpu_load}%")
                print(f"HDD Usage: {response.data.hdd_usage_percentage:.1f}%")
                
                if response.error_message:  # Warnings about critical conditions
                    print(f"🚨 CRITICAL ALERTS: {response.error_message}")
                else:
                    print("✅ All systems are healthy")
        else:
            print(f"❌ Health monitoring failed: {response.error_message}")
    
    def list_monitored_routers(self) -> None:
        """List all monitored routers."""
        routers = self.router_info_repo.list_all_routers()
        
        if not routers:
            print("No routers are currently being monitored.")
            return
        
        print("📋 Monitored Routers:")
        for host, info in routers.items():
            print(f"  • {host} - {info.board_name} ({info.platform}) - Last updated: {info.last_updated}")


# Simple CLI interface
async def main():
    """Main entry point with improved layered architecture."""
    host = environ.get("MIKROTIK_HOST")
    username = environ.get("MIKROTIK_USERNAME")
    password = environ.get("MIKROTIK_PASSWORD")

    if not host or not username or not password:
        print("Please set MIKROTIK_HOST, MIKROTIK_USERNAME, and MIKROTIK_PASSWORD environment variables.")
        return
    controller = RouterMonitoringController(host, username, password)

    # Get system resource information
    await controller.get_system_resource()

    print("\n" + "="*50 + "\n")
    
    # Monitor system health
    await controller.monitor_system_health()

    print("\n" + "="*50 + "\n")
    
    # List monitored routers
    controller.list_monitored_routers()


if __name__ == "__main__":
    asyncio.run(main())