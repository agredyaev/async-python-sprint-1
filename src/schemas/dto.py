from pydantic import BaseModel

from src.schemas.mixins import DateMixin


class CommonDTO(BaseModel):
    location: str


class HourDTO(BaseModel):
    hour: int
    temp: int
    cond_score: int


class DayDTO(DateMixin):
    hours: list[HourDTO]


class ExtractTaskDTO(CommonDTO):
    days: list[DayDTO]


class TransformedDayDTO(DateMixin):
    hours_count: int
    cond_score: int
    temp_avg: float


class TransformTaskDTO(CommonDTO):
    days: list[TransformedDayDTO]
