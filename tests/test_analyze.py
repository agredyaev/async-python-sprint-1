import logging

import pytest

from src.pipeline.analyze import AnalyzeTask
from src.schemas.dto import TransformedDayDTO, TransformTaskDTO


@pytest.fixture
def mock_transformed_data():
    return [
        TransformTaskDTO(
            location="Location A",
            days=[TransformedDayDTO(date="2024-10-10", hours_count=10, cond_score=9, temp_avg=20)],
        ),
        TransformTaskDTO(
            location="Location B",
            days=[TransformedDayDTO(date="2024-10-10", hours_count=10, cond_score=8, temp_avg=18)],
        ),
        TransformTaskDTO(
            location="Location C",
            days=[TransformedDayDTO(date="2024-10-10", hours_count=10, cond_score=7, temp_avg=15)],
        ),
        TransformTaskDTO(
            location="Location D",
            days=[TransformedDayDTO(date="2024-10-10", hours_count=10, cond_score=5, temp_avg=10)],
        ),
    ]


def test_analyze_task_top_3_locations(mock_transformed_data, mocker, caplog):
    mocker.patch("src.core.settings.settings.inpt.temp_weight", 0.7)
    mocker.patch("src.core.settings.settings.inpt.cond_weight", 0.3)
    mocker.patch("src.core.settings.settings.inpt.top_locations_count", 3)
    mocker.patch("src.core.settings.settings.otpt.path", "/mocked_path")

    mocker.patch("polars.DataFrame.write_json")

    # Preparing the mock data
    data_in = (
        {"location": dto.location, "temp_avg": day.temp_avg, "cond_score": day.cond_score}
        for dto in mock_transformed_data
        for day in dto.days
    )

    with caplog.at_level(logging.INFO):
        analyze_task = AnalyzeTask(data_in=data_in)
        analyze_task.run()

    log_output = [record.message for record in caplog.records if "Top locations:" in record.message]
    assert len(log_output) > 0, "Expected top locations to be logged but none found."

    expected_top_3 = ["Location A", "Location B", "Location C"]
    for loc in expected_top_3:
        assert loc in log_output[0], f"Expected {loc} in top locations, but not found."
