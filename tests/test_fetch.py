import pytest

from polyfactory.factories.pydantic_factory import ModelFactory

from src.clients.yandex_weather import YandexWeatherAPI
from src.pipeline.fetch import FetchTask
from src.schemas.weather_response import WeatherResponse


class WeatherResponseFactory(ModelFactory[WeatherResponse]): ...


@pytest.fixture
def weather_response():
    return WeatherResponseFactory.build()


@pytest.fixture
def mock_invalid_data():
    return {"geo_object": {"locality": {"name": "Test City"}}, "fact": {"temp": "invalid_temperature"}}


@pytest.fixture
def mock_missing_forecast():
    return {"geo_object": {"locality": {"name": "Test City"}}, "fact": {"temp": 20}}


def test_fetch_task_invalid_url(mocker):
    mocker.patch.object(YandexWeatherAPI, "get_data", return_value=None)
    fetch_task = FetchTask(data_in=(city for city in ["http://invalid-url.com"]))
    result = fetch_task.process("http://invalid-url.com")
    assert result is None


def test_fetch_task_no_data(mocker):
    mocker.patch.object(YandexWeatherAPI, "get_data", return_value=None)
    fetch_task = FetchTask(data_in=(city for city in ["http://no-data-url.com"]))
    result = fetch_task.process("http://no-data-url.com")
    assert result is None


def test_fetch_task_invalid_data(mock_invalid_data, mocker):
    mocker.patch.object(YandexWeatherAPI, "get_data", return_value=mock_invalid_data)
    fetch_task = FetchTask(data_in=(city for city in ["http://invalid-data-url.com"]))
    result = fetch_task.process("http://invalid-data-url.com")
    assert result is None


def test_fetch_task_missing_forecast(mock_missing_forecast, mocker):
    mocker.patch.object(YandexWeatherAPI, "get_data", return_value=mock_missing_forecast)
    fetch_task = FetchTask(data_in=(city for city in ["http://missing-forecast-url.com"]))
    result = fetch_task.process("http://missing-forecast-url.com")
    assert result is None


def test_fetch_task_success(weather_response, mocker):
    mocker.patch.object(YandexWeatherAPI, "get_data", return_value=weather_response.model_dump())

    fetch_task = FetchTask(data_in=(city for city in ["http://valid-url.com"]))
    result = fetch_task.process("http://valid-url.com")

    assert result is not None
    assert result["geo_object"]["locality"]["name"] == weather_response.geo_object.locality.name
    assert result["fact"]["temp"] == weather_response.fact.temp
