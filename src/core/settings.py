from dotenv import find_dotenv, load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())


class DefaultSettings(BaseSettings):
    """Class to store default project settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class PythonVersionSettings(DefaultSettings):
    """Class to store Python version settings."""

    min_major: int = Field(..., description="Minimum major version")
    min_minor: int = Field(..., description="Minimum minor version")

    model_config = SettingsConfigDict(env_prefix="PYTHON_VER_")


class InputSettings(DefaultSettings):
    day_hours_start: int = Field(..., description="Day hours start")
    day_hours_end: int = Field(..., description="Day hours end")
    hour_conditions_score: str = Field(..., description="Hour conditions score")
    links_path: str = Field(..., description="Links path")
    top_locations_count: int = Field(..., description="Top locations count")
    cond_weight: float = Field(..., description="Condition weights")
    temp_weight: float = Field(..., description="Temperature weights")

    model_config = SettingsConfigDict(env_prefix="INPUT_")


class OutputSettings(DefaultSettings):
    path: str = Field(..., description="Output path")

    model_config = SettingsConfigDict(env_prefix="OUTPUT_")


class Settings(BaseSettings):
    py_ver: PythonVersionSettings = PythonVersionSettings()
    inpt: InputSettings = InputSettings()
    otpt: OutputSettings = OutputSettings()


settings = Settings()
