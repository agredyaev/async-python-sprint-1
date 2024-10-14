from typing import Any

from collections.abc import Generator

import polars as pl

from polars import Expr

from src.core.logger import get_logger
from src.core.settings import settings as s
from src.pipeline.base import BaseTask

logger = get_logger("AnalyzeTask")


class AnalyzeTask(BaseTask):
    """Analyze transformed data."""

    def __init__(self, data_in: Generator[dict[str, Any], None, None]) -> None:
        super().__init__(data_in)

    @staticmethod
    def _normalize_column(df: pl.DataFrame, column_name: str) -> pl.Series:
        """Normalize values in a column to the range [0, 1]."""
        column_series = df.get_column(column_name)

        if column_series.is_empty():
            return column_series

        if not column_series.dtype.is_numeric():
            raise ValueError("Column must be of numeric type")

        return (column_series - column_series.mean()) / column_series.std()

    @staticmethod
    def _get_weighted_sum(col1: str, col2: str, w1: float, w2: float) -> Expr:
        """Calculate the weighted sum of two columns."""
        return (pl.col(col1) * w1).fill_null(0) + (pl.col(col2) * w2).fill_null(0)

    def process(self, item: Any | None = None) -> pl.DataFrame:  # noqa:ARG002
        """Calculate scores for each location based on the transformed data."""

        transformed_data = (pl.DataFrame(item, infer_schema_length=100) for item in self.data_in)
        pr_df = pl.concat(transformed_data, how="vertical")

        pr_df = pr_df.with_columns(
            [
                self._normalize_column(pr_df, "temp_avg").alias("norm_temp_avg"),
                self._normalize_column(pr_df, "cond_score").alias("norm_cond_score"),
            ]
        )

        pr_df = pr_df.with_columns(
            [
                self._get_weighted_sum(
                    "norm_temp_avg", "norm_cond_score", s.inpt.temp_weight, s.inpt.cond_weight
                ).alias("weighted_sum")
            ]
        )
        return pr_df.group_by("location").agg([pl.sum("weighted_sum").alias("score")])

    def run(self, mode: str | None = None) -> Any:  # noqa:ARG002
        top_locations = self.process()
        top_locations = top_locations.sort("score", descending=True).head(s.inpt.top_locations_count)

        top_locations.write_json(s.otpt.path)

        logger.info("Process finished, result saved to %s", s.otpt.path)
        logger.info("Top locations: %s", top_locations)
