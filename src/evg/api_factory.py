"""Factory to create API objects."""
from contextlib import asynccontextmanager
from pathlib import Path

from aiohttp import ClientSession
from evg.api import AioEvergreenApi
from evg.evg_config import EvgConfig


class EvgApiFactory:
    """A factory for creating API clients."""

    def __init__(self, evg_config: EvgConfig) -> None:
        """
        Initialize evergreen api factory.

        :param evg_config: Evergreen API configuration.
        """
        self.evg_config = evg_config

    @classmethod
    def from_file(cls, path: Path) -> "EvgApiFactory":
        """
        Create an API factory from the configuration at the given path.

        :param path: Path to evergreen api configuration.
        :return: Factory to create evergreen API client.
        """
        return cls(EvgConfig.from_file(path))

    @classmethod
    def from_default_config(cls) -> "EvgApiFactory":
        """
        Create an API factory from the configuration at the default path.

        :return: Factory to create evergreen API client.
        """
        return cls(EvgConfig.find_default_config())

    @asynccontextmanager
    async def evergreen_api(self):
        headers = self.evg_config.get_auth_headers()
        async with ClientSession(headers=headers) as session:
            api = AioEvergreenApi(session, self.evg_config.api_server)
            yield api
        api.close()

    def get_evergreen_api_client(self) -> AioEvergreenApi:
        """
        Get a client that needs to be manually closed.

        You should class `close()` on the returned object once finished.
        """
        headers = self.evg_config.get_auth_headers()
        session = ClientSession(headers=headers)
        return AioEvergreenApi(session, self.evg_config.api_server)