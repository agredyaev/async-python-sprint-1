from typing import Any

from collections.abc import Generator

from src.core.logger import get_logger
from src.pipeline.base import BaseTask
from src.schemas.dto import DayDTO, ExtractTaskDTO, HourDTO
from src.schemas.weather_response import WeatherResponse

logger = get_logger("ExtractTask")


class ExtractTask(BaseTask):
    """Extract required data from WeatherResponse objects."""

    def __init__(self, data_in: Generator[dict[str, Any], None, None]) -> None:
        super().__init__(data_in)

    def process(self, item: Any) -> dict[str, Any]:
        item = WeatherResponse(**item)
        days = [
            DayDTO(
                date=forecast.date,
                hours=[
                    HourDTO(hour=int(hour.hour), temp=hour.temp, cond_score=hour.condition.score)
                    for hour in forecast.hours
                    if hour.is_focus
                ],
            )
            for forecast in item.forecasts
        ]

        location = item.geo_object.locality.name
        logger.info("Extracted data for %s", location)
        return ExtractTaskDTO(location=location, days=days).model_dump()
