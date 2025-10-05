from routeros_api import RouterOsApiPool  # pyright: ignore

from app.lib.routeros.types.connection_config import ConnectionConfig


class MikroTikConnectionManager:
    """Manages connections to MikroTik routers."""

    def __init__(self, config: ConnectionConfig):
        self.connection_config = config
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type: type, exc_value: Exception, traceback: object):
        self.disconnect()

    def connect(self):
        """Establish connection to MikroTik router."""
        if not self.connection:
            self.connection = RouterOsApiPool(
                host=self.connection_config.host,
                port=self.connection_config.port,
                username=self.connection_config.username,
                password=self.connection_config.password,
                plaintext_login=True,
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
        return api.get_resource(resource_path)  # pyright: ignore

    def disconnect(self):
        """Disconnect from the router."""
        if self.connection:
            self.connection.disconnect()
            self.connection = None
