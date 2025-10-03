from typing import Dict, Optional
from routeros_api import RouterOsApiPool

from src.domain.entities import SystemResource
from src.domain.repositories import SystemResourceRepository


class MikroTikConnectionManager:
    """Manages connections to MikroTik routers."""
    
    def __init__(self, host: str, username: str, password: str, port: int = 8728):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        """Establish connection to MikroTik router."""
        if not self.connection:
            self.connection = RouterOsApiPool(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                plaintext_login=True
            )

    def get_connection(self):
        """Get the active connection."""
        if not self.connection:
            raise Exception("Not connected to MikroTik router.")
        return self.connection

    def get_resource(self, resource_path: str):
        """Get a specific resource from the router."""
        if not self.connection:
            raise Exception("Not connected to MikroTik router.")
        api = self.connection.get_api()
        return api.get_resource(resource_path)

    def disconnect(self):
        """Disconnect from the router."""
        if self.connection:
            self.connection.disconnect()
            self.connection = None


class MikroTikSystemResourceRepository(SystemResourceRepository):
    """MikroTik implementation of SystemResourceRepository."""
    
    def __init__(self, username: str, password: str, port: int = 8728):
        self.username = username
        self.password = password
        self.port = port

    async def get_system_resource(self, host: str) -> Optional[SystemResource]:
        """Get system resource information from MikroTik router."""
        try:
            with MikroTikConnectionManager(host, self.username, self.password, self.port) as connection:
                resource = connection.get_resource('/system/resource')
                response = resource.get()
                
                if response and isinstance(response, list) and len(response) > 0:
                    data: Dict[str, str] = response[0]
                    if isinstance(data, dict):
                        return self._map_to_domain_entity(data)
                    
                return None
                
        except Exception as e:
            print(f"Error retrieving system resource: {e}")
            return None

    async def check_connection(self, host: str) -> bool:
        """Check if connection to MikroTik router is available."""
        try:
            with MikroTikConnectionManager(host, self.username, self.password, self.port) as connection:
                # Try to get a simple resource to test connection
                resource = connection.get_resource('/system/resource')
                response = resource.get()
                return response is not None
        except Exception:
            return False

    def _map_to_domain_entity(self, data: Dict[str, str]) -> SystemResource:
        """Map MikroTik API response to domain entity."""
        def parse_memory_value(value: str) -> int:
            """Parse memory values like '128MiB' to bytes."""
            if not value:
                return 0
            
            # Remove any trailing characters and convert
            value = value.strip()
            if value.endswith('MiB'):
                return int(float(value[:-3]) * 1024 * 1024)
            elif value.endswith('KiB'):
                return int(float(value[:-3]) * 1024)
            elif value.endswith('GiB'):
                return int(float(value[:-3]) * 1024 * 1024 * 1024)
            else:
                # Try to parse as plain number
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return 0

        def parse_hdd_value(value: str) -> int:
            """Parse HDD values like '128MiB' to bytes."""
            return parse_memory_value(value)

        def parse_percentage(value: str) -> int:
            """Parse percentage values like '15%' to integer."""
            if not value:
                return 0
            try:
                return int(value.strip('%'))
            except (ValueError, AttributeError):
                return 0

        def parse_int_value(value: str) -> int:
            """Parse integer values safely."""
            if not value:
                return 0
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0

        return SystemResource(
            uptime=data.get('uptime', ''),
            version=data.get('version', ''),
            build_time=data.get('build-time', ''),
            factory_firmware=data.get('factory-firmware', ''),
            free_memory=parse_memory_value(data.get('free-memory', '0')),
            total_memory=parse_memory_value(data.get('total-memory', '0')),
            cpu=data.get('cpu', ''),
            cpu_count=parse_int_value(data.get('cpu-count', '0')),
            cpu_frequency=data.get('cpu-frequency', ''),
            cpu_load=parse_percentage(data.get('cpu-load', '0')),
            free_hdd_space=parse_hdd_value(data.get('free-hdd-space', '0')),
            total_hdd_space=parse_hdd_value(data.get('total-hdd-space', '0')),
            write_sector_total=parse_int_value(data.get('write-sector-total', '0')),
            write_sector_since_reboot=parse_int_value(data.get('write-sector-since-reboot', '0')),
            bad_blocks=parse_int_value(data.get('bad-blocks', '0')),
            architecture_name=data.get('architecture-name', ''),
            board_name=data.get('board-name', ''),
            platform=data.get('platform', '')
        )