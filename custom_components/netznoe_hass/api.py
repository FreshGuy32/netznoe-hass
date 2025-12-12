"""Sample API Client."""

from __future__ import annotations

import socket
from typing import TYPE_CHECKING, Any

import aiohttp
import async_timeout

if TYPE_CHECKING:
    from datetime import date


class NetzNoeApiClientError(Exception):
    """Exception to indicate a general API error."""


class NetzNoeApiClientCommunicationError(
    NetzNoeApiClientError,
):
    """Exception to indicate a communication error."""


class NetzNoeApiClientAuthenticationError(
    NetzNoeApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise NetzNoeApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class NetzNoeApiClient:
    """Sample API Client."""

    _base_url = "https://smartmeter.netz-noe.at"

    def __init__(
        self,
        username: str,
        password: str,
        meter_id: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._meter_id = meter_id
        self._session = session

    async def async_login(self) -> Any:
        """Log into the api."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method="POST",
                    url=f"{self._base_url}/orchestration/Authentication/Login",
                    headers={},
                    json={
                        "user": self._username,
                        "pwd": self._password,
                    },
                )
                _verify_response_or_raise(response)

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise NetzNoeApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise NetzNoeApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise NetzNoeApiClientError(
                msg,
            ) from exception

    async def async_get_data(self, day: date) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                await self.async_login()

            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method="GET",
                    url=f"{self._base_url}/orchestration/ConsumptionRecord/Day?meterId={self._meter_id}&day={day.isoformat()}",
                    headers={},
                    json={
                        "user": self._username,
                        "pwd": self._password,
                    },
                )
                _verify_response_or_raise(response)

                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise NetzNoeApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise NetzNoeApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise NetzNoeApiClientError(
                msg,
            ) from exception
