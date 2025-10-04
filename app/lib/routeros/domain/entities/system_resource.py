from dataclasses import dataclass


@dataclass
class SystemResource:
    """Core domain entity representing system resource information."""

    uptime: str
    version: str
    build_time: str
    factory_firmware: str
    free_memory: int
    total_memory: int
    cpu: str
    cpu_count: int
    cpu_frequency: str
    cpu_load: int
    free_hdd_space: int
    total_hdd_space: int
    write_sector_total: int
    write_sector_since_reboot: int
    bad_blocks: int
    architecture_name: str
    board_name: str
    platform: str

    @property
    def memory_usage_percentage(self) -> float:
        """Calculate memory usage percentage."""
        if self.total_memory == 0:
            return 0.0
        return ((self.total_memory - self.free_memory) / self.total_memory) * 100

    @property
    def hdd_usage_percentage(self) -> float:
        """Calculate HDD usage percentage."""
        if self.total_hdd_space == 0:
            return 0.0
        return (
            (self.total_hdd_space - self.free_hdd_space) / self.total_hdd_space
        ) * 100

    @property
    def is_memory_critical(self) -> bool:
        """Check if memory usage is critical (>90%)."""
        return self.memory_usage_percentage > 90

    @property
    def is_cpu_critical(self) -> bool:
        """Check if CPU usage is critical (>90%)."""
        return self.cpu_load > 90
