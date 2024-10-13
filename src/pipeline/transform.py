from typing import Any

from collections.abc import Generator

import polars as pl

from src.core.logger import get_logger
from src.pipeline.base import BaseTask
from src.schemas.dto import ExtractTaskDTO, TransformedDayDTO, TransformTaskDTO

logger = get_logger("TransformTask")


class TransformTask(BaseTask):
    """Transform extracted data."""

    def __init__(self, data_in: Generator[dict[str, Any], None, None]) -> None:
        super().__init__(data_in)

    @staticmethod
    def _transform(item: TransformTaskDTO) -> dict[str, Any]:
        """
        Transform data to dataframe.
        Args:
            item (TransformTaskDTO): Data to transform.
        Returns:
            dict[str, Any]: Transformed data.
        """
        location_df = pl.DataFrame({"location": [item.location] * len(item.days)})
        days_df = pl.DataFrame([day.model_dump() for day in item.days])
        result = pl.concat([location_df, days_df], how="horizontal")

        return result.to_dict()

    def process(self, item: Any) -> dict[str, Any]:
        item = ExtractTaskDTO(**item)
        days = [
            TransformedDayDTO(
                date=day.date,
                hours_count=len(day.hours),
                cond_score=sum(hour.cond_score for hour in day.hours),
                temp_avg=sum(hour.temp for hour in day.hours) / (len(day.hours) or 1),
            )
            for day in item.days
        ]
        transform_dto = TransformTaskDTO(location=item.location, days=days)
        result = self._transform(transform_dto)
        logger.info("Transformed data for %s", item.location)
        return result
