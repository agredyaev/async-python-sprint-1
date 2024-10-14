from ast import literal_eval
from enum import StrEnum, auto

from src.core.settings import settings as s

score = literal_eval(s.inpt.hour_conditions_score)


class Condition(StrEnum):
    clear = auto()
    partly_cloudy = "partly-cloudy"
    cloudy = auto()
    overcast = auto()
    drizzle = auto()
    light_rain = "light-rain"
    light_snow = "light-snow"
    wet_snow = "wet-snow"
    rain = auto()
    showers = auto()
    snow = auto()
    snow_showers = "snow-showers"
    moderate_rain = "moderate-rain"
    heavy_rain = "heavy-rain"
    continuous_heavy_rain = "continuous-heavy-rain"
    hail = auto()
    thunderstorm = auto()
    thunderstorm_with_rain = "thunderstorm-with-rain"
    thunderstorm_with_hail = "thunderstorm-with-hail"
    unknown = auto()

    @property
    def score(self) -> int:
        return score.get(self.name, 0)
