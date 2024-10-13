from typing import Any

from http import HTTPStatus

import httpx

from pydantic_core import from_json

from src.core.exceptions import HTTPRequestError
from src.core.logger import get_logger

logger = get_logger("YandexWeatherAPI")


class YandexWeatherAPI:
    """Base class for handling weather-related requests."""

    __slots__ = ("url",)

    def __init__(self, url: str) -> None:
        self.url = url

    def _do_req(self) -> httpx.Response:
        """Asynchronous request method using httpx."""
        response = httpx.get(self.url)

        if response.status_code != HTTPStatus.OK:
            raise HTTPRequestError(f"Error during request. {response.status_code}: {response.reason_phrase}")

        return response

    def get_data(self) -> dict[str, Any] | None:
        """Asynchronous method for getting data from API."""
        try:
            response = self._do_req()
            return from_json(response.read())
        except (httpx.RequestError, HTTPRequestError, ValueError) as ex:
            logger.exception("Request to %s failed", self.url, exc_info=ex)
            return None
