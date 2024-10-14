from pydantic import BaseModel, Field

from src.schemas.condition import Condition


class WeatherDataMixin(BaseModel):
    temp: int = Field(lt=80, description="Temperature")
    feels_like: int
    icon: str
    condition: Condition = Field(default=Condition.unknown, description="Condition with default unknown")
    cloudness: float
    prec_type: int
    prec_strength: float
    prec_prob: int
    is_thunder: bool
    wind_speed: float
    wind_dir: str
    pressure_mm: int
    pressure_pa: int
    humidity: int
    uv_index: int
    soil_temp: int | None = None
    soil_moisture: float | None = None
    wind_gust: float | None = None


class DateMixin(BaseModel):
    date: str
