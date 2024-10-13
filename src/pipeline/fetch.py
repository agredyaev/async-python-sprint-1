from typing import Any

from collections.abc import Generator

from src.clients.yandex_weather import YandexWeatherAPI
from src.core.logger import get_logger
from src.pipeline.base import BaseTask
from src.schemas.weather_response import WeatherResponse

logger = get_logger("FetchTask")


class FetchTask(BaseTask):
    """Fetch data from the API."""

    def __init__(self, data_in: Generator[str, None, None]) -> None:
        super().__init__(data_in)

    def process(self, item: str) -> dict[str, Any] | None:
        api = YandexWeatherAPI(item)
        data = api.get_data()

        if data is None:
            logger.error("Data not found for city: %s", item)
            return None
        try:
            validated_data = WeatherResponse(**data)
            logger.info("Fetched data for %s", validated_data.geo_object.locality.name)
            return validated_data.model_dump()
        except ValueError:
            logger.exception("Data not valid for city: %s", item)
            return None
