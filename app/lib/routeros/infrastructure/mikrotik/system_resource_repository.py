from app.lib.routeros.domain.entities import SystemResource
from app.lib.routeros.domain.repositories import SystemResourceRepository
from app.lib.routeros.infrastructure.mikrotik import MikroTikConnectionManager
from app.lib.routeros.infrastructure.mikrotik.constant import MikrotikResourceUri
from app.lib.routeros.infrastructure.mikrotik.types import MikrotikConnectionConfig


class MikroTikSystemResourceRepository(SystemResourceRepository):
    """MikroTik implementation of SystemResourceRepository."""

    def __init__(self, connection_config: MikrotikConnectionConfig):
        self.connection_config = connection_config

    async def get_system_resource(self) -> SystemResource | None:
        """Get system resource information from MikroTik router."""
        try:
            with MikroTikConnectionManager(self.connection_config) as connection:
                resource = connection.get_resource(MikrotikResourceUri.SYSTEM_RESOURCE)
                response = resource.get()

                if response and isinstance(response, list) and len(response) > 0:
                    data: dict[str, str] = response[0]
                    if isinstance(data, dict):
                        return self._map_to_domain_entity(data)

                return None

        except Exception as e:
            print(f"Error retrieving system resource: {e}")
            return None

    async def check_connection(self) -> bool:
        """Check if connection to MikroTik router is available."""
        try:
            with MikroTikConnectionManager(self.connection_config) as connection:
                # Try to get a simple resource to test connection
                resource = connection.get_resource(MikrotikResourceUri.SYSTEM_RESOURCE)
                response = resource.get()
                return response is not None
        except Exception:
            return False

    def _map_to_domain_entity(self, data: dict[str, str]) -> SystemResource:
        """Map MikroTik API response to domain entity."""

        def parse_memory_value(value: str) -> int:
            """Parse memory values like '128MiB' to bytes."""
            if not value:
                return 0

            # Remove any trailing characters and convert
            value = value.strip()
            if value.endswith("MiB"):
                return int(float(value[:-3]) * 1024 * 1024)
            elif value.endswith("KiB"):
                return int(float(value[:-3]) * 1024)
            elif value.endswith("GiB"):
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
                return int(value.strip("%"))
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
            uptime=data.get("uptime", ""),
            version=data.get("version", ""),
            build_time=data.get("build-time", ""),
            factory_firmware=data.get("factory-firmware", ""),
            free_memory=int(data.get("free-memory", "0")),
            total_memory=int(data.get("total-memory", "0")),
            cpu=data.get("cpu", ""),
            cpu_count=parse_int_value(data.get("cpu-count", "0")),
            cpu_frequency=float(data.get("cpu-frequency", "0")),
            cpu_load=parse_percentage(data.get("cpu-load", "0")),
            free_hdd_space=int(data.get("free-hdd-space", "0")),
            total_hdd_space=parse_hdd_value(data.get("total-hdd-space", "0")),
            write_sector_total=parse_int_value(data.get("write-sector-total", "0")),
            write_sector_since_reboot=parse_int_value(
                data.get("write-sector-since-reboot", "0")
            ),
            bad_blocks=parse_int_value(data.get("bad-blocks", "0")),
            architecture_name=data.get("architecture-name", ""),
            board_name=data.get("board-name", ""),
            platform=data.get("platform", ""),
        )
