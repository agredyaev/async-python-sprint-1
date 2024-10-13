from pydantic import BaseModel

from src.core.settings import settings as s
from src.schemas.mixins import WeatherDataMixin


class Tzinfo(BaseModel):
    name: str
    abbr: str
    dst: bool
    offset: int


class Info(BaseModel):
    n: bool
    geoid: int
    url: str
    lat: float
    lon: float
    tzinfo: Tzinfo
    def_pressure_mm: int
    def_pressure_pa: int
    slug: str
    zoom: int
    nr: bool
    ns: bool
    nsr: bool
    p: bool
    f: bool
    _h: bool


class Location(BaseModel):
    id: int
    name: str


class GeoObject(BaseModel):
    district: Location | None = None
    locality: Location
    province: Location | None = None
    country: Location | None = None


class Yesterday(BaseModel):
    temp: int


class Fact(WeatherDataMixin):
    obs_time: int
    uptime: int
    daytime: str
    polar: bool
    season: str
    source: str


class Hour(WeatherDataMixin):
    hour: str
    hour_ts: int
    prec_mm: float
    prec_period: int

    @property
    def is_focus(self) -> bool:
        return bool(s.inpt.day_hours_start <= int(self.hour) and s.inpt.day_hours_end)


class Biomet(BaseModel):
    index: int
    condition: str


class Forecast(BaseModel):
    date: str
    date_ts: int
    week: int
    sunrise: str
    sunset: str
    rise_begin: str
    set_end: str
    moon_code: int
    moon_text: str
    hours: list[Hour]
    biomet: Biomet | None = None


class WeatherResponse(BaseModel):
    now: int
    now_dt: str
    info: Info
    geo_object: GeoObject
    yesterday: Yesterday
    fact: Fact | None = None
    forecasts: list[Forecast]
